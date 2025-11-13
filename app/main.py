from fastapi import FastAPI

# ...existing config package files expected under app.config...
from app.config.logging_config import setup_logging
from app.config.settings import settings

# example feature router
from app.features.example_feature.router import router as example_router


def create_app() -> FastAPI:
    setup_logging("DEBUG" if settings.DEBUG else "INFO")
    app = FastAPI(title=settings.APP_NAME)

    # Include feature routers
    app.include_router(example_router, prefix="/example", tags=["example"])

    return app


app = create_app()

