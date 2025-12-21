from pydantic import BaseModel, EmailStr, Field

from app.features.users.domain.models import UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=64,
    )
    role: UserRole
    full_name: str
