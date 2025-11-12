import pytest
from fastapi.testclient import TestClient

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app
from database import Base, engine, db
from models import User
import bcrypt


client = TestClient(app)

#Do testowania: pytest tests/app_tests.py -v


@pytest.fixture(autouse=True) #usuwanie i tworzenie bazy danych na nowo FIXTURE
def setup_db():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    hashed_pw = bcrypt.hashpw("admin".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    admin_user = User(username="admin", hashed_password=hashed_pw, role="ROLE_ADMIN")
    db.add(admin_user)
    db.commit()

    hashed_pw2 = bcrypt.hashpw("user".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    normal_user = User(username="user", hashed_password=hashed_pw2, role="ROLE_USER")
    db.add(normal_user)
    db.commit()


def pobierz_naglowek(username, password):
    response = client.post("/login", json={"username": username, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


#testy dla /login
def test_login():
    #dobre
    response = client.post("/login", json={"username": "admin", "password": "admin"})
    assert response.status_code == 200

    #zle
    response2 = client.post("/login", json={"username": "admin", "password": "123"})
    assert response2.status_code == 401

    #nie ma uzytkowniak
    response3 = client.post("/login", json={"username": "123", "password": "123"})
    assert response3.status_code == 401


#testy dla /users
def test_create_user_admin():
    headers = pobierz_naglowek("admin", "admin")
    response = client.post("/users", json={"username": "nowy", "password": "nowy"}, headers=headers)
    assert response.status_code == 200


def test_create_user_by_user():
    headers = pobierz_naglowek("user", "user")
    response = client.post("/users", json={"username": "nowy1", "password": "nowy1"}, headers=headers)
    assert response.status_code == 403


#testy dla /user_details
def test_user_token():
    headers = pobierz_naglowek("user", "user")
    response = client.get("/user_details", headers=headers)
    assert response.status_code == 200


def test_no_token():
    response = client.get("/user_details")
    assert response.status_code == 401

