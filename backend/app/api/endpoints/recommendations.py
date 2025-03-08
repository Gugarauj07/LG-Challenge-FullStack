from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, schemas
from app.api import deps
from app.services.recommendation import get_recommendations_for_user, get_similar_movies
from app.models.movie import movie_genre

router = APIRouter()

@router.get("/user", response_model=List[schemas.Movie])
def get_user_recommendations(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    limit: int = 10
) -> Any:
    """
    Obtém recomendações de filmes para o usuário autenticado
    """
    # Verificar se o usuário tem avaliações suficientes
    rating_count = db.query(models.Rating).filter(models.Rating.user_id == current_user.id).count()
    if rating_count < 5:
        raise HTTPException(
            status_code=400,
            detail="Você precisa avaliar pelo menos 5 filmes para receber recomendações personalizadas"
        )

    # Obter recomendações para o usuário
    movie_ids = get_recommendations_for_user(db, current_user.id, limit)

    # Obter informações completas dos filmes recomendados
    movies = (
        db.query(models.Movie)
        .filter(models.Movie.id.in_(movie_ids))
        .all()
    )

    return movies

@router.get("/similar/{movie_id}", response_model=List[schemas.Movie])
def get_similar_movies_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    movie_id: int,
    limit: int = 10
) -> Any:
    """
    Obtém filmes similares ao filme especificado
    """
    # Verificar se o filme existe
    movie = db.query(models.Movie).filter(models.Movie.movie_id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")

    # Usar a abordagem baseada em gêneros que testamos e funciona
    if movie.genres:
        # Obter gêneros do filme
        genre_ids = [genre.id for genre in movie.genres]

        # Encontrar filmes com gêneros semelhantes
        similar_movies = (
            db.query(models.Movie)
            .join(movie_genre)
            .filter(movie_genre.c.genre_id.in_(genre_ids))
            .filter(models.Movie.id != movie.id)  # Excluir o próprio filme
            .group_by(models.Movie.id)
            .order_by(func.count().desc())  # Ordenar por número de gêneros em comum
            .limit(limit)
        ).all()

        return similar_movies
    else:
        # Se o filme não tiver gêneros, retornar filmes populares
        popular_movies = (
            db.query(models.Movie)
            .join(models.Rating)
            .group_by(models.Movie.id)
            .order_by(func.avg(models.Rating.rating).desc())
            .filter(models.Movie.id != movie.id)
            .limit(limit)
        ).all()

        return popular_movies