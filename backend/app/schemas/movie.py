from typing import List, Optional
from pydantic import BaseModel

# Schema para gênero
class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True

# Schema para filme
class MovieBase(BaseModel):
    title: str
    year: Optional[int] = None
    imdb_id: Optional[str] = None
    tmdb_id: Optional[str] = None

class MovieCreate(MovieBase):
    movie_id: int
    genres: List[str]

class Movie(MovieBase):
    id: int
    movie_id: int
    genres: List[Genre]
    average_rating: Optional[float] = 0.0
    rating_count: Optional[int] = 0

    class Config:
        from_attributes = True

# Schema para lista de filmes com paginação
class MovieList(BaseModel):
    items: List[Movie]
    total: int

# Schema para estatísticas de filmes
class MovieStats(BaseModel):
    total_movies: int
    total_ratings: int
    average_rating: float
    top_genres: List[dict]