from typing import Any

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class DomainError(Exception):
    def __init__(self, status: int, title: str, detail: str, error_type: str) -> None:
        self.status = status
        self.title = title
        self.detail = detail
        self.error_type = error_type


def problem_response(
    request: Request, *, status: int, title: str, detail: Any, error_type: str
) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        media_type="application/problem+json",
        content={
            "type": f"https://errors.example.com/{error_type}",
            "title": title,
            "status": status,
            "detail": jsonable_encoder(detail),
            "instance": str(request.url.path),
            "request_id": getattr(request.state, "request_id", "unknown"),
        },
    )


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def handle_domain_error(request: Request, exc: DomainError) -> JSONResponse:
        return problem_response(
            request,
            status=exc.status,
            title=exc.title,
            detail=exc.detail,
            error_type=exc.error_type,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return problem_response(
            request,
            status=422,
            title="Validation error",
            detail=exc.errors(),
            error_type="validation",
        )
