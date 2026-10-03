#app/services/auth_service.py

# pyright: reportMissingImports=false
from typing import TypeAlias

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SQLAlchemySession

from app.core.exceptions import ConflictException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)

Session: TypeAlias = SQLAlchemySession

def register_user(
    db: Session,
    name: str,
    email: str,
    password: str,
):
    if db is None:
        raise ValueError("Database session is required")

    normalized_name = name.strip()
    if not normalized_name:
        raise ValueError("Name is required")

    normalized_email = email.strip().lower()
    if not normalized_email:
        raise ValueError("Email is required")

    if not password:
        raise ValueError("Password is required")

    existing_user = db.execute(
        text("SELECT 1 FROM users WHERE email = :email"),
        {"email": normalized_email},
    ).first()
    if existing_user:
        raise ConflictException("Email already registered")

    password_hash = hash_password(password)
    try:
        db.execute(
            text(
                "INSERT INTO users (name, email, password_hash) "
                "VALUES (:name, :email, :password_hash)"
            ),
            {
                "name": normalized_name,
                "email": normalized_email,
                "password_hash": password_hash,
            },
        )
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ConflictException("Email already registered") from exc

    return {
        "name": normalized_name,
        "email": normalized_email,
        "password_hash": password_hash,
    }

def authenticate_user(
    db: Session,
    email: str,
    password: str,
):
    if db is None:
        raise ValueError("Database session is required")

    normalized_email = email.strip().lower()
    if not normalized_email:
        raise ValueError("Email is required")

    if not password:
        raise ValueError("Password is required")

    user = db.execute(
        text("SELECT id, password_hash FROM users WHERE email = :email"),
        {"email": normalized_email},
    ).mappings().first()
    if user is None or not verify_password(password, user["password_hash"]):
        raise ValueError("Invalid credentials")

    return {
        "access_token": create_access_token(str(user["id"])),
        "refresh_token": create_refresh_token(str(user["id"])),
        "token_type": "bearer",
    }
