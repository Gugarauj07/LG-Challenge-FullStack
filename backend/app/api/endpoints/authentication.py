from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 token de login para acessar os recursos protegidos da API
    """
    # Verificar se existe um usuário com o username fornecido
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Nome de usuário ou senha incorretos")
    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Nome de usuário ou senha incorretos")

    # Gerar token de acesso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=schemas.User)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Registrar um novo usuário
    """
    # Verificar se já existe um usuário com o mesmo username ou email
    db_user_by_username = db.query(models.User).filter(models.User.username == user_in.username).first()
    if db_user_by_username:
        raise HTTPException(status_code=400, detail="Nome de usuário já registrado")
    if user_in.email:
        db_user_by_email = db.query(models.User).filter(models.User.email == user_in.email).first()
        if db_user_by_email:
            raise HTTPException(status_code=400, detail="Email já registrado")

    # Criar um novo usuário
    user = models.User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model=schemas.User)
def read_users_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Obter informações do usuário atual
    """
    return current_user