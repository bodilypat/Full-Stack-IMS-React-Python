# app/middleware/error_handler.py
# pyright: reportMissingImports=false

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppException


logger = logging.getLogger(__name__)


def _error_response(
    status_code: int,
    code: str,
    message: str,
    details: object = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": code,
                "message": message,
                "details": details,
            },
        },
    )


def register_exception_handlers(
    app: FastAPI,
) -> None:

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException,
    ):
        logger.debug("App exception for %s", request.url.path)
        return _error_response(
            status_code=exc.status_code,
            code=exc.code,
            message=exc.message,
            details=exc.details,
        )

    @app.exception_handler(
        RequestValidationError
    )
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        logger.debug("Validation error for %s", request.url.path)
        return _error_response(
            status_code=422,
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details=exc.errors(),
        )

    @app.exception_handler(
        StarletteHTTPException
    )
    async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException,
    ):
        logger.debug("HTTP exception for %s", request.url.path)
        return _error_response(
            status_code=exc.status_code,
            code="HTTP_ERROR",
            message=str(exc.detail),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.debug("Unhandled exception for %s", request.url.path)
        logger.exception(
            "Unhandled exception",
            exc_info=exc,
        )

        return _error_response(
            status_code=500,
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred",
        )
