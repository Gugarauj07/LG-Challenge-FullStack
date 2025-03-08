from sqlalchemy import Column, Integer, Float, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from app.database.session import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    rating = Column(Float)
    timestamp = Column(BigInteger, nullable=True)

    # Relacionamentos
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")