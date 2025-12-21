import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, func, UUID, Enum
from sqlmodel import Field, SQLModel
from uuid_extensions import uuid7

from app.features.users.domain.models import UserRole


class Account(SQLModel, table=True):
    __tablename__ = "accounts"

    id: uuid.UUID = Field(
        default_factory=uuid7,
        sa_column=Column(UUID(as_uuid=True), primary_key=True),
    )
    email: str = Field(
        max_length=255,
        sa_column=Column(String(255), unique=True, index=True, nullable=False),
    )
    hashed_password: str = Field(nullable=False)
    role: UserRole = Field(
        default=UserRole.STUDENT,
        sa_column=Column(Enum(UserRole, name="user_role"), nullable=False)
    )
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
        )
    )
