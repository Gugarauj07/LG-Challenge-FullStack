from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.session import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), index=True)

    # Garantir que cada usuário só possa favoritar um filme uma vez
    __table_args__ = (
        UniqueConstraint('user_id', 'movie_id', name='uix_user_movie_favorite'),
    )

    # Relacionamentos
    user = relationship("User", back_populates="favorites")
    movie = relationship("Movie", back_populates="favorited_by")