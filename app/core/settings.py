from anyio.functools import lru_cache
from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # APP SETTINGS
    APP_NAME: str = "Thesis Hub"
    ENV: str = Field(
        default="development", description="development | staging | production"
    )
    DEBUG: bool = True

    HOST: str
    PORT: int

    SECRET_KEY: str

    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    DATABASE_URL: AnyUrl | None = None
    DATABASE_URL_SYNC: AnyUrl

    # CORS
    CORS_ORIGINS: list[str] = []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def async_database_url(self) -> str:
        if self.DATABASE_URL is None:
            return (
                "postgresql+asyncpg://"
                + self.POSTGRES_USER
                + ":"
                + self.POSTGRES_PASSWORD
                + "@"
                + self.POSTGRES_HOST
                + ":"
                + self.POSTGRES_PORT
                + "/"
                + self.POSTGRES_DB
            )

        return str(self.DATABASE_URL)

    @property
    def is_dev(self) -> bool:
        return self.ENV == "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()
