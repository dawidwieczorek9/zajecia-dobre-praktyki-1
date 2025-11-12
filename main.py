from typing import Optional

import bcrypt
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from database import db, engine, Base
from models import User
from datetime import datetime, timedelta
import jwt


app = FastAPI()
SECRET_KEY = "super_secret_key" # w praktyce trzymane w zmiennych środowiskowych
ALGORITHM = "HS256"

Base.metadata.create_all(bind=engine)


class LoginData(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    password: str


def authorization_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Brak nagłówka")

    try: #podzielenie naglowka na nazwe i token
        header_name, token = authorization.split()
        if header_name.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Zła nazwa nagłówka (nie ma Bearer)")
    except ValueError:
        raise HTTPException(status_code=401, detail="Zły format nagłówka")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub") #użytkownik
        role = payload.get("role") #rola uzytkownika
        if not username or not role:
            raise HTTPException(status_code=401, detail="Brak użytkownika lub roli")
        return {"username": username, "role": role}

    except Exception:
        raise HTTPException(status_code=401, detail="Coś złego w tokenie")


@app.post("/login")
def login(data: LoginData):
    username = data.username
    password = data.password.encode('utf-8')
    """if username not in USERS_DB:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    hashed_pw = USERS_DB[username]
    if not bcrypt.checkpw(password, hashed_pw):
        raise HTTPException(status_code=401, detail="Invalid credentials")"""

    #do bazy zapytanie
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not user.verify_password(data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
    "sub": user.username,
    "role": user.role,
    "iat": datetime.utcnow(),
    "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/users")
def create_user(user_data: UserCreate, current_user: dict = Depends(authorization_user)):
    #sprawdza, czy uzytkownik jest adminem, tylko on moze dodawać innych uzytkownikow
    if current_user["role"] != "ROLE_ADMIN":
        raise HTTPException(status_code=403, detail="Only admins can create users")
    #Czy user istenieje
    exists = db.query(User).filter(User.username == user_data.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    new_user = User(username=user_data.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"Uzytkownik stworzony: '{user_data.username}'"}


#skonczone na punkcie 4 (zrobiony)
# TESTOWANIE PRZEZ localhost:8000/docs - swagger UI


@app.get("/user_details")  #Depends - mechanizm zależności
def get_user_details(current_user: dict = Depends(authorization_user)):

    return {"zalogowany jako: ": current_user["username"]}


#STWORZONY ADMIN: admin, hasło: admin123



