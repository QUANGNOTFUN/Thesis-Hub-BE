from passlib.exc import PasswordSizeError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.features.auth.domain.models import Account
from app.features.auth.domain.schemas import RegisterRequest
from app.features.users.domain.models import User


class AuthService:
    @staticmethod
    async def register(
        db: AsyncSession,
        payload: RegisterRequest,
    ) -> Account:

        result = await db.execute(
            select(Account).where(Account.email == payload.email) # type: ignore[arg-type]
        )
        if result.scalar_one_or_none():
            raise ValueError("Email already registered")

        hashed_password = hash_password(payload.password)

        account = Account(
            email=payload.email,
            hashed_password=hashed_password,
            role=payload.role,
        )

        user = User(
            id=account.id
        )

        try:
            db.add(account)
            db.add(user)
            await db.commit()
            await db.refresh(account)
            await db.refresh(user)

        except Exception:
            await db.rollback()
            raise

        return account

    @staticmethod
    async def login(
            db: AsyncSession,
            email: str,
            password: str,
    ) -> Account:
        result = await db.execute(
            select(Account).where(Account.email == email) # type: ignore[arg-type]
        )
        account = result.scalar_one_or_none()
        if not account or account.password != password:
            raise ValueError("Invalid credentials")

        return account
