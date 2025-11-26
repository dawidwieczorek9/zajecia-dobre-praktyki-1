from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Movies(Base):
    __tablename__ = "movies"

    movieId: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]]
    genres: Mapped[Optional[str]]

    #ratings: Mapped[list["Ratings"]] = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")
    #tags: Mapped[list["Tags"]] = relationship("Tag", back_populates="movie", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Movie(movieId={self.movieId!r}, title={self.title!r}, genres={self.genres!r})"


class Links(Base):
    __tablename__ = "links"

    movieId: Mapped[int] = mapped_column(primary_key=True)
    imdbId: Mapped[str] = mapped_column(String(30))
    tmdbId: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Link(movieId={self.movieId!r}, imdbId={self.imdbId!r}, tmdbId={self.tmdbId!r})"


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