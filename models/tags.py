from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Tags(Base):
    __tablename__ = "tags"

    userId: Mapped[int] = mapped_column(primary_key=True)
    movieId: Mapped[int] = mapped_column(ForeignKey("movies.movieId"), primary_key=True)
    tag: Mapped[Optional[str]] = mapped_column(primary_key=True)
    timestamp: Mapped[Optional[str]]

    #movie: Mapped["Movies"] = relationship("Movies", back_populates="tags")

    def __repr__(self) -> str:
        return f"Tag(userId={self.userId!r}, movieId={self.movieId!r}, tag={self.tag!r}, timestamp={self.timestamp!r})"
