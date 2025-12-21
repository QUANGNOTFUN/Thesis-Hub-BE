from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.router import api_routers
from app.core.openapi import apply_bearer_security
from app.core.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    # enable Swagger UI and ReDoc (defaults are /docs and /redoc)
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        description="Thesis Hub API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Include feature routers
    app.include_router(api_routers)

    # Apply OpenAPI bearer security customization
    apply_bearer_security(app)

    return app


app = create_app()
