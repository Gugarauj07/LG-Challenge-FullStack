from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.database.session import Base

# Tabela associativa para relacionamento muitos-para-muitos entre filmes e gêneros
movie_genre = Table(
    "movie_genre",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, unique=True, index=True)  # ID original do MovieLens
    title = Column(String, index=True)
    year = Column(Integer, index=True, nullable=True)
    imdb_id = Column(String, nullable=True)
    tmdb_id = Column(String, nullable=True)

    # Relacionamentos
    genres = relationship("Genre", secondary=movie_genre, back_populates="movies")
    ratings = relationship("Rating", back_populates="movie")
    tags = relationship("Tag", back_populates="movie")
    favorited_by = relationship("Favorite", back_populates="movie")

    @property
    def average_rating(self):
        if not self.ratings or len(self.ratings) == 0:
            return 0.0
        return sum(r.rating for r in self.ratings) / len(self.ratings)

    @property
    def rating_count(self):
        return len(self.ratings)


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Relacionamentos
    movies = relationship("Movie", secondary=movie_genre, back_populates="genres")