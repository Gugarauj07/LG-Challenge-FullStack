from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from app.database.session import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    tag = Column(String)
    timestamp = Column(BigInteger, nullable=True)

    # Relacionamentos
    user = relationship("User", back_populates="tags")
    movie = relationship("Movie", back_populates="tags")