from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.knowledge_bases import router as knowledge_base_router
from app.api.routes.repos import router as repos_router
from app.core.config import get_settings
from app.core.exceptions import (
    AppError,
    app_error_handler,
    generic_exception_handler,
    validation_exception_handler,
)


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="GitHub Cloud Connector",
        version="1.0.0",
        description="A FastAPI backend that authenticates with GitHub using a PAT and exposes repository and issue actions.",
    )

    allowed_origins = [settings.frontend_origin, "http://127.0.0.1:5173"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(dict.fromkeys(allowed_origins)),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.settings = settings
    app.include_router(health_router)
    app.include_router(repos_router)
    app.include_router(knowledge_base_router)
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    return app


app = create_app()
