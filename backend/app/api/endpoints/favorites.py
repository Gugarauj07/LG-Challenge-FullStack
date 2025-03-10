from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Movie])
def read_favorites(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Recupera todos os filmes favoritos do usuário atual.
    """
    favorites = (
        db.query(models.Movie)
        .join(models.Favorite)
        .filter(models.Favorite.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return favorites


@router.post("/{movie_id}", response_model=schemas.Favorite)
def add_favorite(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    movie_id: int
) -> Any:
    """
    Adiciona um filme aos favoritos do usuário.
    """
    # Verificar se o filme existe
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Filme não encontrado"
        )

    # Criar o favorito
    favorite = models.Favorite(
        user_id=current_user.id,
        movie_id=movie_id
    )

    try:
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        return favorite
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Este filme já está nos favoritos"
        )


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    movie_id: int
) -> None:
    """
    Remove um filme dos favoritos do usuário.
    """
    favorite = (
        db.query(models.Favorite)
        .filter(models.Favorite.user_id == current_user.id, models.Favorite.movie_id == movie_id)
        .first()
    )
    if not favorite:
        raise HTTPException(
            status_code=404,
            detail="Filme não encontrado nos favoritos"
        )

    db.delete(favorite)
    db.commit()