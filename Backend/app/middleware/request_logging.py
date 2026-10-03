#app/middleware/request_logging.py

import logging
import time
import uuid

from fastapi import FastAPI, Request  # type: ignore[import-not-found]


logger = logging.getLogger("app.request")


def configure_request_logging(
    app: FastAPI,
) -> None:

    @app.middleware("http")
    async def request_logging_middleware(
        request: Request,
        call_next,
    ):
        request_id = str(uuid.uuid4())

        request.state.request_id = request_id

        start_time = time.perf_counter()
        client_host = (
            request.client.host
            if request.client is not None
            else "unknown"
        )

        logger.info(
            "Incoming request %s %s request_id=%s client=%s",
            request.method,
            request.url.path,
            request_id,
            client_host,
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client": client_host,
                "event": "request_started",
            },
        )

        try:
            response = await call_next(request)

            elapsed = (
                time.perf_counter() - start_time
            )

            response.headers[
                "X-Request-ID"
            ] = request_id

            logger.info(
                "%s %s -> %s %.3fs request_id=%s",
                request.method,
                request.url.path,
                response.status_code,
                elapsed,
                request_id,
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": round(elapsed * 1000, 2),
                    "client": client_host,
                    "event": "request_completed",
                },
            )

            return response

        except Exception:
            elapsed = (
                time.perf_counter() - start_time
            )

            logger.exception(
                "%s %s -> ERROR %.3fs request_id=%s",
                request.method,
                request.url.path,
                elapsed,
                request_id,
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": 500,
                    "duration_ms": round(elapsed * 1000, 2),
                    "client": client_host,
                    "event": "request_failed",
                },
            )

            raise
