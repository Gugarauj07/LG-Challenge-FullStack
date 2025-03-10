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
    Obtém recomendações de filmes para o usuário autenticado.
    Prioriza recomendações baseadas nos favoritos do usuário,
    mas também considera avaliações se disponíveis.
    """
    # Verificar se o usuário tem favoritos
    favorite_count = db.query(models.Favorite).filter(models.Favorite.user_id == current_user.id).count()

    if favorite_count > 0:
        # Obter IDs dos filmes favoritos do usuário
        favorite_movies = (
            db.query(models.Movie)
            .join(models.Favorite)
            .filter(models.Favorite.user_id == current_user.id)
            .all()
        )

        # Obter gêneros dos filmes favoritos
        favorite_genres = set()
        for movie in favorite_movies:
            for genre in movie.genres:
                favorite_genres.add(genre.id)

        # Encontrar filmes semelhantes baseados nos gêneros favoritos, excluindo os já favoritados
        favorite_movie_ids = [movie.id for movie in favorite_movies]
        recommendations = (
            db.query(models.Movie)
            .join(movie_genre)
            .filter(movie_genre.c.genre_id.in_(favorite_genres))
            .filter(~models.Movie.id.in_(favorite_movie_ids))  # Excluir filmes já favoritados
            .group_by(models.Movie.id)
            .order_by(func.count().desc())  # Ordenar por número de gêneros em comum
            .limit(limit)
        ).all()

        if recommendations:
            return recommendations

    # Se não há favoritos ou não conseguimos recomendações baseadas neles,
    # verificar avaliações
    rating_count = db.query(models.Rating).filter(models.Rating.user_id == current_user.id).count()
    if rating_count < 5:
        # Se não há avaliações suficientes, retornar filmes populares
        popular_movies = (
            db.query(models.Movie)
            .join(models.Rating)
            .group_by(models.Movie.id)
            .order_by(func.avg(models.Rating.rating).desc())
            .limit(limit)
        ).all()
        return popular_movies

    # Se há avaliações suficientes, usar o método de recomendação colaborativa
    movie_ids = get_recommendations_for_user(db, current_user.id, limit)
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