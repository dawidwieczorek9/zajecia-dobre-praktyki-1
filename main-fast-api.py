from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import csv

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
    rating: Optional[str] = None
    timestamp: Optional[str] = None


class Tag(BaseModel):
    userId: int
    movieId: int
    tag: Optional[str] = None
    timestamp: Optional[str] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/links")
def read_links():
    links = []
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
    return links


@app.get("/movies")
def read_movies():
    movies = []
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
    return movies


@app.get("/ratings")
def read_ratings():
    ratings = []
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
    return ratings


@app.get("/tags")
def read_tags():
    tags = []
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
    return tags
