from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Links(Base):
    __tablename__ = "links"

    movieId: Mapped[int] = mapped_column(primary_key=True)
    imdbId: Mapped[str] = mapped_column(String(30))
    tmdbId: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Link(movieId={self.movieId!r}, imdbId={self.imdbId!r}, tmdbId={self.tmdbId!r})"
