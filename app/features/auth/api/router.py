from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.features.auth.domain.schemas import RegisterRequest
from app.features.auth.service.auth_service import AuthService

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await AuthService.register(
            db=db,
            payload=payload,
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="User login",
)
async def login(
    payload: dict,
    db: AsyncSession = Depends(get_db),
):
    # Login logic to be implemented
    return {"message": "User logged in successfully"}