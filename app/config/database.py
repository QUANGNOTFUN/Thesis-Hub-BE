from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings

# Sync SQLAlchemy engine (change to async if your project uses async drivers)
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    FastAPI dependency to get a DB session.

    Usage in route:
    from fastapi import Depends
    def endpoint(db: Session = Depends(get_db)): ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
import logging
from logging.config import dictConfig


def setup_logging(level: str = "INFO") -> None:
    """
    Call this early (e.g. in FastAPI startup) to configure structured console logs.
    """
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": level,
                }
            },
            "root": {"level": level, "handlers": ["console"]},
        }
    )

# Example usage:
# from app.config.logging_config import setup_logging
# setup_logging(level="DEBUG")

