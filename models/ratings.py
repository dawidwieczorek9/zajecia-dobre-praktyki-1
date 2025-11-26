from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Ratings(Base):
    __tablename__ = "rating"

    userId: Mapped[int] = mapped_column(primary_key=True)
    movieId: Mapped[int] = mapped_column(ForeignKey("movies.movieId"), primary_key=True)
    rating: Mapped[Optional[str]]
    timestamp: Mapped[Optional[str]]

    #movie: Mapped["Movies"] = relationship("Movies", back_populates="ratings")

    def __repr__(self) -> str:
        return f"Rating(userId={self.userId!r}, movieId={self.movieId!r}, rating={self.rating!r}, timestamp={self.timestamp!r})"
