# app/middleware/cors.py
import os

from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware  # pyright: ignore[reportMissingImports]


def configure_cors(app: FastAPI) -> None:
    allowed_origins = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ALLOWED_ORIGINS", "http://localhost:5173"
        ).split(",")
        if origin.strip()
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "Accept"],
    )
