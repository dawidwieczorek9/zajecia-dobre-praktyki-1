import csv

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import Optional, List
from sqlalchemy.orm import relationship
from sqlalchemy import String, ForeignKey, create_engine


class Base(DeclarativeBase):
    pass


class Links(Base):
    __tablename__ = "links"

    movieId: Mapped[int] = mapped_column(primary_key=True)
    imdbId: Mapped[str] = mapped_column(String(30))
    tmdbId: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Link(movieId={self.movieId!r}, imdbId={self.imdbId!r}, tmdbId={self.tmdbId!r})"


class Movies(Base):
    __tablename__ = "movies"

    movieId: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]]
    genres: Mapped[Optional[str]]

    #ratings: Mapped[list["Ratings"]] = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")
    #tags: Mapped[list["Tags"]] = relationship("Tag", back_populates="movie", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Movie(movieId={self.movieId!r}, title={self.title!r}, genres={self.genres!r})"


class Ratings(Base):
    __tablename__ = "rating"

    userId: Mapped[int] = mapped_column(primary_key=True)
    movieId: Mapped[int] = mapped_column(ForeignKey("movies.movieId"), primary_key=True)
    rating: Mapped[Optional[str]]
    timestamp: Mapped[Optional[str]]

    #movie: Mapped["Movies"] = relationship("Movies", back_populates="ratings")

    def __repr__(self) -> str:
        return f"Rating(userId={self.userId!r}, movieId={self.movieId!r}, rating={self.rating!r}, timestamp={self.timestamp!r})"


class Tags(Base):
    __tablename__ = "tags"

    userId: Mapped[int] = mapped_column(primary_key=True)
    movieId: Mapped[int] = mapped_column(ForeignKey("movies.movieId"), primary_key=True)
    tag: Mapped[Optional[str]] = mapped_column(primary_key=True)
    timestamp: Mapped[Optional[str]]

    #movie: Mapped["Movies"] = relationship("Movies", back_populates="tags")

    def __repr__(self) -> str:
        return f"Tag(userId={self.userId!r}, movieId={self.movieId!r}, tag={self.tag!r}, timestamp={self.timestamp!r})"


def load_data():
    with Session(engine) as session:
        if session.query(Links).first() is None:
            with open("links.csv", newline="") as csvfile:
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
            with open("movies.csv", newline="", encoding="utf-8") as csvfile:
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
            with open("ratings.csv", newline="") as csvfile:
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
            with open("tags.csv", newline="") as csvfile:
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



engine = create_engine("sqlite:///database.db", echo=True)
Base.metadata.create_all(engine)
load_data()

#teraz do zrobienia - zmapowanie wyników plików do bazy danych (pobranie tych danych z csv do json przy pomocy main-fast-api



