from fastapi import APIRouter

from app.features.auth.api.router import router as auth_router

api_routers = APIRouter(prefix="/api/v1")

api_routers.include_router(router=auth_router, prefix="/auth", tags=["auth"])
