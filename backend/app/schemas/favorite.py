from typing import Optional

from pydantic import BaseModel


# Esquema base para Favorite
class FavoriteBase(BaseModel):
    movie_id: int


# Esquema para criar um novo Favorite
class FavoriteCreate(FavoriteBase):
    pass


# Esquema para atualizar um Favorite
class FavoriteUpdate(FavoriteBase):
    pass


# Esquema para representar um Favorite no banco de dados
class FavoriteInDBBase(FavoriteBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# Esquema para retornar um Favorite
class Favorite(FavoriteInDBBase):
    pass