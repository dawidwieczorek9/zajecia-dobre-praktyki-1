from fastapi import HTTPException, status

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import csv
from fastapi import Depends

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


from models.links import Links
from models.movies import Movies
from models.ratings import Ratings
from models.tags import Tags

app = FastAPI()

#Użyłem biblioteki Pydantic, tak jak było w załączonym do lekcji poradniku zamiast __dict__


class Link(BaseModel):
    movieId: int
    imdbId: Optional[str] = None
    tmdbId: Optional[str] = None


class Movie(BaseModel):
    movieId: int
    title: Optional[str] = None
    genres: Optional[str] = None


class Rating(BaseModel):
    userId: int
    movieId: int
    rating: Optional[float] = None
    timestamp: Optional[str] = None


class Tag(BaseModel):
    userId: int
    movieId: int
    tag: Optional[str] = None
    timestamp: Optional[str] = None


engine = create_engine("sqlite:///database.db", echo=True)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/links")
def read_links():
    # Stary kod
    """links = []
    with open("links.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            link = Link(
                movieId=int(row[0]),
                imdbId=row[1],
                tmdbId=row[2]
            )
            links.append(link)
    return links"""
    #Nowy kod po refaktoryzacji
    db = SessionLocal()
    try:
        links = db.query(Links).all()
        return links
    finally:
        db.close()


@app.get("/movies")
def read_movies():

    """movies = []
    with open("movies.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            movie = Movie(
                movieId=int(row[0]),
                title=row[1],
                genres=row[2]
            )
            movies.append(movie)
    return movies"""

    db = SessionLocal()
    try:
        movies = db.query(Movies).all()
        return movies
    finally:
        db.close()


@app.get("/ratings")
def read_ratings():
    """ratings = []
    with open("ratings.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            rating = Rating(
                userId=int(row[0]),
                movieId=int(row[1]),
                rating=row[2],
                timestamp=row[3]
            )
            ratings.append(rating)
    return ratings"""

    db = SessionLocal()
    try:
        ratings = db.query(Ratings).all()
        return ratings
    finally:
        db.close()


@app.get("/tags")
def read_tags():
    """tags = []
    with open("tags.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            tag = Tag(
                userId=int(row[0]),
                movieId=int(row[1]),
                tag=row[2],
                timestamp=row[3]
            )
            tags.append(tag)
    return tags"""
    db = SessionLocal()
    try:
        tags = db.query(Tags).all()
        return tags
    finally:
        db.close()


#CRUD - links
@app.post("/links", response_model=Link, status_code=status.HTTP_201_CREATED)
def create_link(link: Link, db: Session = Depends(get_db)):
    db_obj = Links(**link.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@app.get("/links/{movie_id}", response_model=Link)
def read_link(movie_id: int, db: Session = Depends(get_db)):
    obj = db.query(Links).filter(Links.movieId == movie_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie ma linku")
    return obj


@app.put("/links/{movie_id}", response_model=Link)
def update_link(movie_id: int, link: Link, db: Session = Depends(get_db)):
    obj = db.query(Links).filter(Links.movieId == movie_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie ma linku")
    for key, value in link.model_dump().items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/links/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(movie_id: int, db: Session = Depends(get_db)):
    obj = db.query(Links).filter(Links.movieId == movie_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie ma linku")
    db.delete(obj)
    db.commit()


#CRUD - movies
@app.post("/movies", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie, db: Session = Depends(get_db)):
    db_obj = Movies(**movie.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@app.get("/movies/{movie_id}", response_model=Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    obj = db.query(Movies).filter(Movies.movieId == movie_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie ma filmu")
    return obj


@app.put("/movies/{movie_id}", response_model=Movie)
def update_movie(movie_id: int, movie: Movie, db: Session = Depends(get_db)):
    obj = db.query(Movies).filter(Movies.movieId == movie_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie ma filmu")

    for key, value in movie.model_dump().items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    obj = db.query(Movies).filter(Movies.movieId == movie_id).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie ma filmu")
    db.delete(obj)
    db.commit()


#CRUD - ratings
@app.post("/ratings", response_model=Rating, status_code=status.HTTP_201_CREATED)
def create_rating(rating: Rating, db: Session = Depends(get_db)):
    db_obj = Ratings(**rating.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@app.get("/ratings/{user_id}/{movie_id}", response_model=Rating)
def read_rating(user_id: int, movie_id: int, db: Session = Depends(get_db)):
    obj = db.query(Ratings).filter(
        Ratings.userId == user_id,
        Ratings.movieId == movie_id
    ).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie ma ratingu")
    return obj


@app.put("/ratings/{user_id}/{movie_id}", response_model=Rating)
def update_rating(user_id: int, movie_id: int, rating: Rating, db: Session = Depends(get_db)):
    obj = db.query(Ratings).filter(
        Ratings.userId == user_id,
        Ratings.movieId == movie_id
    ).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie ma ratingu")

    for key, value in rating.model_dump().items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/ratings/{user_id}/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(user_id: int, movie_id: int, db: Session = Depends(get_db)):
    obj = db.query(Ratings).filter(
        Ratings.userId == user_id,
        Ratings.movieId == movie_id
    ).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie ma ratingu")
    db.delete(obj)
    db.commit()


#CRUD - tags
@app.post("/tags", response_model=Tag, status_code=status.HTTP_201_CREATED)
def create_tag(tag: Tag, db: Session = Depends(get_db)):
    db_obj = Tags(**tag.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@app.get("/tags/{user_id}/{movie_id}", response_model=Tag)
def read_tag(user_id: int, movie_id: int, db: Session = Depends(get_db)):
    obj = db.query(Tags).filter(
        Tags.userId == user_id,
        Tags.movieId == movie_id
    ).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie ma tagu")
    return obj


@app.put("/tags/{user_id}/{movie_id}", response_model=Tag)
def update_tag(user_id: int, movie_id: int, tag: Tag, db: Session = Depends(get_db)):
    obj = db.query(Tags).filter(
        Tags.userId == user_id,
        Tags.movieId == movie_id
    ).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie ma tagu")

    for key, value in tag.model_dump().items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/tags/{user_id}/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(user_id: int, movie_id: int, db: Session = Depends(get_db)):
    obj = db.query(Tags).filter(
        Tags.userId == user_id,
        Tags.movieId == movie_id
    ).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie ma tagu")
    db.delete(obj)
    db.commit()