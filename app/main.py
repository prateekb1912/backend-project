from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.middleware import require_auth


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.name,
        version=settings.version,
        debug=settings.debug,
    )
    application.middleware("http")(require_auth)
    application.include_router(api_router)
    return application


app = create_app()
