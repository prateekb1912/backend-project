from fastapi import APIRouter

from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.user import router as user_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(health_router, tags=["health"])
api_router.include_router(user_router)
