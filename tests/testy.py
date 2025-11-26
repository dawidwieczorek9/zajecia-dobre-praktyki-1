import os
import shutil
import sqlite3

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from starlette import status

from main_fast_api import get_db, app

from models.movies import Movies, Links, Ratings, Tags, Base


TEST_SQLALCHEMY_URL = "sqlite:///database_test.db"
TABLES = [Movies, Links, Ratings, Tags]

initial_movies_data = [
    {"movieId": 1, "title": "Toy Story (1995)", "genres": "Adventure|Animation|Children|Comedy|Fantasy"},
    {"movieId": 2, "title": "Jumanji (1995)", "genres": "Adventure|Children|Fantasy"},
    {"movieId": 3, "title": "Grumpier Old Men (1995)", "genres": "Comedy|Romance"},
    {"movieId": 4, "title": "Waiting to Exhale (1995)", "genres": "Comedy|Drama|Romance"},
    {"movieId": 5, "title": "Father of the Bride Part II (1995)", "genres": "Comedy"},
    {"movieId": 6, "title": "Heat (1995)", "genres": "Action|Crime|Thriller"},
    {"movieId": 7, "title": "Sabrina (1995)", "genres": "Comedy|Romance"},
    {"movieId": 8, "title": "Tom and Huck (1995)", "genres": "Adventure|Children"},
    {"movieId": 9, "title": "Sudden Death (1995)", "genres": "Action"},
    {"movieId": 10, "title": "GoldenEye (1995)", "genres": "Action|Adventure|Thriller"}
]

initial_links_data = [
    {"movieId": 1, "imdbId": "0114709", "tmdbId": "862"},
    {"movieId": 2, "imdbId": "0113497", "tmdbId": "8844"},
    {"movieId": 3, "imdbId": "0113228", "tmdbId": "15602"},
    {"movieId": 4, "imdbId": "0114885", "tmdbId": "31357"},
    {"movieId": 5, "imdbId": "0113041", "tmdbId": "11862"},
    {"movieId": 6, "imdbId": "0113277", "tmdbId": "949"},
    {"movieId": 7, "imdbId": "0114319", "tmdbId": "11860"},
    {"movieId": 8, "imdbId": "0112302", "tmdbId": "45325"},
    {"movieId": 9, "imdbId": "0114576", "tmdbId": "9091"},
    {"movieId": 10, "imdbId": "0113189", "tmdbId": "710"}
]

initial_ratings_data = [
    {"userId": 1, "movieId": 1, "rating": 4.0, "timestamp": "964982703"},
    {"userId": 1, "movieId": 3, "rating": 4.0, "timestamp": "964981247"},
    {"userId": 1, "movieId": 6, "rating": 4.0, "timestamp": "964982224"},
    {"userId": 1, "movieId": 4, "rating": 5.0, "timestamp": "964983815"},
    {"userId": 1, "movieId": 5, "rating": 5.0, "timestamp": "964982931"},
    {"userId": 2, "movieId": 7, "rating": 3.0, "timestamp": "964982400"},
    {"userId": 2, "movieId": 8, "rating": 5.0, "timestamp": "964980868"},
    {"userId": 2, "movieId": 9, "rating": 4.0, "timestamp": "964982176"},
    {"userId": 3, "movieId": 2, "rating": 5.0, "timestamp": "964984041"},
    {"userId": 3, "movieId": 10, "rating": 5.0, "timestamp": "964984100"}
]

initial_tags_data = [
    {"userId": 2, "movieId": 1, "tag": "funny", "timestamp": "1445714994"},
    {"userId": 2, "movieId": 1, "tag": "Highly quotable", "timestamp": "1445714996"},
    {"userId": 2, "movieId": 2, "tag": "will ferrell", "timestamp": "1445714992"},
    {"userId": 2, "movieId": 3, "tag": "Boxing story", "timestamp": "1445715207"},
    {"userId": 2, "movieId": 4, "tag": "MMA", "timestamp": "1445715200"},
    {"userId": 2, "movieId": 5, "tag": "Tom Hardy", "timestamp": "1445715205"},
    {"userId": 2, "movieId": 6, "tag": "drugs", "timestamp": "1445715054"},
    {"userId": 2, "movieId": 7, "tag": "Leonardo DiCaprio", "timestamp": "1445715051"},
    {"userId": 2, "movieId": 8, "tag": "Martin Scorsese", "timestamp": "1445715056"},
    {"userId": 7, "movieId": 9, "tag": "way too long", "timestamp": "1169687325"}
]


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        TEST_SQLALCHEMY_URL,
        connect_args={"check_same_thread": False}
    )
    return engine


@pytest.fixture(scope="session")
def TestingSessionLocal(test_engine):
    return sessionmaker(bind=test_engine)


@pytest.fixture(scope="function")
def override_get_db(TestingSessionLocal):
    def _override():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    return _override


@pytest.fixture(scope="function")
def db_session(test_engine, TestingSessionLocal):
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()
    try:
        db.add_all([Movies(**data) for data in initial_movies_data])
        db.add_all([Links(**data) for data in initial_links_data])
        db.add_all([Ratings(**data) for data in initial_ratings_data])
        db.add_all([Tags(**data) for data in initial_tags_data])
        db.commit()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(override_get_db, db_session):
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


#CRUD - movies

def test_read_movies_list(client):
    response = client.get("/movies")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert isinstance(data, list)


def test_read_movie_item_success(client):
    response = client.get("/movies/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["movieId"] == 1


def test_read_movie_item_not_found(client):
    response = client.get("/movies/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_movie(client):
    new_movie = {
        "movieId": 9999,
        "title": "Test Film",
        "genres": "Action"
    }
    response = client.post("/movies", json=new_movie)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "Test Film"
    response_get = client.get("/movies/9999")
    assert response_get.status_code == status.HTTP_200_OK


def test_update_movie(client):
    update_data = {
        "movieId": 1,
        "title": "Zmieniony Tytuł",
        "genres": "Drama"
    }
    response = client.put("/movies/1", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Zmieniony Tytuł"


def test_delete_movie(client):
    response = client.delete("/movies/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response_get = client.get("/movies/1")
    assert response_get.status_code == status.HTTP_404_NOT_FOUND

#CRUD - ratings

def test_read_ratings_list(client):
    response = client.get("/ratings")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)


def test_read_rating_item_success(client):
    new_rating = {
        "ratingId": 5001,
        "userId": 1,
        "movieId": 1,
        "rating": 4.5,
        "timestamp": 123456
    }
    client.post("/ratings", json=new_rating)

    response = client.get("/ratings/5001")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["ratingId"] == 5001


def test_read_rating_item_not_found(client):
    response = client.get("/ratings/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_rating(client):
    new_rating = {
        "ratingId": 5002,
        "userId": 2,
        "movieId": 1,
        "rating": 3.0,
        "timestamp": 987654
    }
    response = client.post("/ratings", json=new_rating)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["rating"] == 3.0
    response_get = client.get("/ratings/5002")
    assert response_get.status_code == status.HTTP_200_OK


def test_update_rating(client):
    new_rating = {
        "ratingId": 5003,
        "userId": 3,
        "movieId": 2,
        "rating": 2.0,
        "timestamp": 111111
    }
    client.post("/ratings", json=new_rating)

    update_data = {
        "ratingId": 5003,
        "userId": 3,
        "movieId": 2,
        "rating": 5.0,
        "timestamp": 222222
    }
    response = client.put("/ratings/5003", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["rating"] == 5.0


def test_delete_rating(client):
    new_rating = {
        "ratingId": 5004,
        "userId": 4,
        "movieId": 2,
        "rating": 1.0,
        "timestamp": 333333
    }
    client.post("/ratings", json=new_rating)

    response = client.delete("/ratings/5004")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response_get = client.get("/ratings/5004")
    assert response_get.status_code == status.HTTP_404_NOT_FOUND


#CRUD - links

def test_read_links_list(client):
    response = client.get("/links")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_read_link_item_success(client):
    new_link = {
        "movieId": 6001,
        "imdbId": "12345",
        "tmdbId": "54321"
    }
    client.post("/links", json=new_link)

    response = client.get("/links/6001")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["movieId"] == 6001


def test_read_link_item_not_found(client):
    response = client.get("/links/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_link(client):
    new_link = {
        "movieId": 6002,
        "imdbId": "abcde",
        "tmdbId": "edcba"
    }
    response = client.post("/links", json=new_link)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["movieId"] == 6002

    response_get = client.get("/links/6002")
    assert response_get.status_code == status.HTTP_200_OK


def test_update_link(client):
    new_link = {
        "movieId": 6003,
        "imdbId": "11111",
        "tmdbId": "22222"
    }
    client.post("/links", json=new_link)

    update_data = {
        "movieId": 6003,
        "imdbId": "99999",
        "tmdbId": "88888"
    }
    response = client.put("/links/6003", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["imdbId"] == "99999"


def test_delete_link(client):
    new_link = {
        "movieId": 6004,
        "imdbId": "foo",
        "tmdbId": "bar"
    }
    client.post("/links", json=new_link)

    response = client.delete("/links/6004")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response_get = client.get("/links/6004")
    assert response_get.status_code == status.HTTP_404_NOT_FOUND


#CRUD - tags

def test_read_tags_list(client):
    response = client.get("/tags")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_read_tag_item_success(client):
    new_tag = {
        "tagId": 7001,
        "userId": 10,
        "movieId": 20,
        "tag": "funny",
        "timestamp": 123123
    }
    client.post("/tags", json=new_tag)

    response = client.get("/tags/7001")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["tagId"] == 7001


def test_read_tag_item_not_found(client):
    response = client.get("/tags/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_tag(client):
    new_tag = {
        "tagId": 7002,
        "userId": 11,
        "movieId": 21,
        "tag": "cool",
        "timestamp": 555555
    }
    response = client.post("/tags", json=new_tag)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["tag"] == "cool"

    response_get = client.get("/tags/7002")
    assert response_get.status_code == status.HTTP_200_OK


def test_update_tag(client):
    new_tag = {
        "tagId": 7003,
        "userId": 12,
        "movieId": 22,
        "tag": "old",
        "timestamp": 888888
    }
    client.post("/tags", json=new_tag)

    update_data = {
        "tagId": 7003,
        "userId": 12,
        "movieId": 22,
        "tag": "updated",
        "timestamp": 999999
    }
    response = client.put("/tags/7003", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["tag"] == "updated"


def test_delete_tag(client):
    new_tag = {
        "tagId": 7004,
        "userId": 13,
        "movieId": 23,
        "tag": "remove",
        "timestamp": 111111
    }
    client.post("/tags", json=new_tag)

    response = client.delete("/tags/7004")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response_get = client.get("/tags/7004")
    assert response_get.status_code == status.HTTP_404_NOT_FOUND