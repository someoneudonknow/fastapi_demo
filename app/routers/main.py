from fastapi import APIRouter

from app.routers.auth_router import auth_router
from app.routers.user_router import user_router

app_router = APIRouter(prefix="/api/v1")

app_router.include_router(user_router)
app_router.include_router(auth_router)
