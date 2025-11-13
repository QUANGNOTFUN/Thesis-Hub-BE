from typing import List, Optional
from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Thesis Hub"
    ENV: str = "development"
    DEBUG: bool = True

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Security
    SECRET_KEY: str  # required: set in .env or environment

    # Database
    DATABASE_URL: str  # e.g. postgresql://user:pass@host:5432/dbname

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def is_production(self) -> bool:
        return self.ENV.lower() == "production"


# single settings instance to import elsewhere
settings = Settings()

