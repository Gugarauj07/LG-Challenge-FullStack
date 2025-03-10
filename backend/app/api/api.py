from fastapi import APIRouter

from app.api.endpoints import movies, authentication, recommendations, favorites

api_router = APIRouter()
api_router.include_router(authentication.router, prefix="/auth", tags=["auth"])
api_router.include_router(movies.router, prefix="/movies", tags=["movies"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["favorites"])