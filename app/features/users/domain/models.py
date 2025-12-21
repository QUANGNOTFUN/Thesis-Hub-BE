import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, func, DateTime, UUID
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import SQLModel, Field


class UserRole(str, Enum):
    ADMIN = "admin"
    LECTURER = "lecturer"
    STUDENT = "student"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        foreign_key="accounts.id",
        primary_key=True,
    )
    full_name: str = Field(max_length=40, nullable=True)
    birth_date: str = Field(max_length=10, nullable=True)
    major: str = Field(max_length=50, nullable=True)
    course_id: list[str] = Field(
        sa_column=Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    )
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
        ),
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
        ),
    )
