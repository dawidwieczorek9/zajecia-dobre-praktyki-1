from typing import Optional
from sqlalchemy import String
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