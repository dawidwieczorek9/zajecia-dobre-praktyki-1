import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models.links import Links, Base
from models.movies import Movies
from models.ratings import Ratings
from models.tags import Tags

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")


def load_data():
    with Session(engine) as session:
        if session.query(Links).first() is None:
            with open("database/links.csv", newline="") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    link = Links(
                        movieId=int(row[0]),
                        imdbId=row[1],
                        tmdbId=row[2] if row[2] else None
                    )
                    session.add(link)

        if session.query(Movies).first() is None:
            with open("database/movies.csv", newline="", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    movie = Movies(
                        movieId=int(row[0]),
                        title=row[1],
                        genres=row[2]
                    )
                    session.add(movie)

        if session.query(Ratings).first() is None:
            with open("database/ratings.csv", newline="") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    rating = Ratings(
                        userId=int(row[0]),
                        movieId=int(row[1]),
                        rating=row[2],
                        timestamp=row[3]
                    )
                    session.add(rating)

        if session.query(Tags).first() is None:
            with open("database/tags.csv", newline="") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    tag = Tags(
                        userId=int(row[0]),
                        movieId=int(row[1]),
                        tag=row[2],
                        timestamp=row[3]
                    )
                    session.add(tag)

        session.commit()
        print("Dane zostały pobrane do bazy")


engine = create_engine(f"sqlite:///{db_path}", echo=True)
Base.metadata.create_all(engine)
load_data()