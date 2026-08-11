import json
import logging
import time
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.api.health import router as health_router
from app.api.projects import router as projects_router
from app.config import Settings, get_settings
from app.database import create_database_engine
from app.errors import install_error_handlers
from app.models import Base

logger = logging.getLogger("company_app")


def configure_logging(level: str) -> None:
    logging.basicConfig(level=level, format="%(message)s")


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.engine = create_database_engine(resolved)
        if resolved.auto_create_schema:
            Base.metadata.create_all(app.state.engine)
        yield
        app.state.engine.dispose()

    app = FastAPI(
        title=resolved.app_name,
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        redoc_url=None,
    )
    app.state.settings = resolved
    configure_logging(resolved.log_level)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=resolved.allowed_hosts)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "X-Request-ID"],
    )

    @app.middleware("http")
    async def request_context(request: Request, call_next: object) -> object:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        started = time.perf_counter()
        response = await call_next(request)  # type: ignore[operator]
        response.headers["X-Request-ID"] = request_id
        logger.info(
            json.dumps(
                {
                    "event": "request",
                    "method": request.method,
                    "path": request.url.path,
                    "status": response.status_code,
                    "duration_ms": round((time.perf_counter() - started) * 1000, 2),
                    "request_id": request_id,
                }
            )
        )
        return response

    install_error_handlers(app)
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(projects_router, prefix="/api/v1")
    return app


app = create_app()
