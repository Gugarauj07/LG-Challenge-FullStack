from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, desc
from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.api import deps

router = APIRouter()

@router.get("/search", response_model=schemas.MovieList)
def search_movies(
    *,
    db: Session = Depends(deps.get_db),
    title: Optional[str] = None,
    year: Optional[int] = None,
    genre: Optional[str] = None,
    genres: Optional[List[str]] = Query(None),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Buscar filmes por título, ano e/ou gênero(s).
    """
    query = db.query(models.Movie).options(joinedload(models.Movie.genres))

    if title:
        query = query.filter(models.Movie.title.ilike(f"%{title}%"))

    if year:
        query = query.filter(models.Movie.year == year)

    # Para manter compatibilidade com versões anteriores, mantemos o suporte para um único gênero
    if genre and not genres:
        genres = [genre]

    if genres:
        for genre_name in genres:
            genre_obj = db.query(models.Genre).filter(models.Genre.name == genre_name).first()
            if genre_obj:
                query = query.filter(models.Movie.genres.any(models.Genre.id == genre_obj.id))
            else:
                # Se um dos gêneros não existe, continuamos com os outros
                continue

    total = query.count()
    movies = query.order_by(models.Movie.title).offset(skip).limit(limit).all()

    return {"items": movies, "total": total}

@router.get("/top-rated", response_model=List[schemas.Movie])
def get_top_rated_movies(
    *,
    db: Session = Depends(deps.get_db),
    limit: int = Query(10, ge=1, le=100),
) -> Any:
    """
    Retorna os K filmes mais bem avaliados.
    """
    # Subconsulta para calcular a média de avaliações por filme
    subquery = (
        db.query(
            models.Rating.movie_id,
            func.avg(models.Rating.rating).label("avg_rating"),
            func.count(models.Rating.id).label("rating_count")
        )
        .group_by(models.Rating.movie_id)
        .subquery()
    )

    # Consulta principal para obter os filmes mais bem avaliados
    # com um mínimo de 5 avaliações
    query = (
        db.query(models.Movie)
        .join(subquery, models.Movie.id == subquery.c.movie_id)
        .filter(subquery.c.rating_count >= 5)
        .options(joinedload(models.Movie.genres))
        .order_by(desc(subquery.c.avg_rating))
        .limit(limit)
    )

    return query.all()

@router.get("/by-id/{movie_id}", response_model=schemas.Movie)
def get_movie_by_id(
    *,
    db: Session = Depends(deps.get_db),
    movie_id: int,
) -> Any:
    """
    Obtém detalhes de um filme pelo ID.
    """
    movie = db.query(models.Movie).options(joinedload(models.Movie.genres)).filter(models.Movie.movie_id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return movie

@router.get("/stats", response_model=schemas.MovieStats)
def get_movie_stats(
    *,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Obtém estatísticas gerais sobre os filmes.
    """
    total_movies = db.query(func.count(models.Movie.id)).scalar()
    total_ratings = db.query(func.count(models.Rating.id)).scalar()
    avg_rating = db.query(func.avg(models.Rating.rating)).scalar() or 0.0

    # Obter os 10 gêneros mais populares
    genre_counts = (
        db.query(
            models.Genre.name,
            func.count(models.movie_genre.c.movie_id).label("movie_count")
        )
        .join(models.movie_genre, models.Genre.id == models.movie_genre.c.genre_id)
        .group_by(models.Genre.name)
        .order_by(desc("movie_count"))
        .limit(10)
        .all()
    )

    top_genres = [
        {"name": genre[0], "movie_count": genre[1]}
        for genre in genre_counts
    ]

    return {
        "total_movies": total_movies,
        "total_ratings": total_ratings,
        "average_rating": float(avg_rating),
        "top_genres": top_genres
    }