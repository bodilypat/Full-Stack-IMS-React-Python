#app/core/security.py

from datetime import datetime, timedelta, timezone
from typing import Any

try:
    from jose import jwt  # type: ignore[reportMissingImports]
except ImportError:  # pragma: no cover
    jwt = None  # type: ignore[assignment]

try:
    from pwdlib import PasswordHash  # type: ignore[reportMissingImports]
except ImportError:  # pragma: no cover
    PasswordHash = None  # type: ignore[assignment]

try:
    from app.core.config import settings  # type: ignore[reportMissingImports]
except ImportError:  # pragma: no cover
    settings = None  # type: ignore[assignment]

ALGORITHM = "HS256"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

class _MissingDependencyError(RuntimeError):
    pass

if settings is None:
    class _Settings:
        ACCESS_TOKEN_EXPIRE_MINUTES = 30
        REFRESH_TOKEN_EXPIRE_DAYS = 7
        SECRET_KEY = "change-me"
        JWT_ALGORITHM = ALGORITHM

    settings = _Settings()

if PasswordHash is None:
    class _PasswordHash:
        @staticmethod
        def recommended():
            raise _MissingDependencyError("pwdlib is required to hash passwords")

    password_hash = _PasswordHash().recommended()
else:
    password_hash = PasswordHash.recommended()

def _get_secret_key() -> str:
    secret_key = getattr(settings, "SECRET_KEY", None)
    if not secret_key:
        raise ValueError("SECRET_KEY is not configured")
    return str(secret_key)

def _get_algorithm() -> str:
    return str(getattr(settings, "JWT_ALGORITHM", ALGORITHM))

def hash_password(password: str) -> str:
    if PasswordHash is None:
        raise _MissingDependencyError("pwdlib is required to hash passwords")
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string")
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    if PasswordHash is None:
        raise _MissingDependencyError("pwdlib is required to verify passwords")
    if not isinstance(password, str) or not isinstance(hashed_password, str):
        return False
    if not password or not hashed_password:
        return False
    return password_hash.verify(password, hashed_password)

def _create_token(subject: str, token_type: str, expires_delta: timedelta) -> str:
    if jwt is None:
        raise _MissingDependencyError("python-jose is required to create JWT tokens")
    if not isinstance(subject, str) or not subject:
        raise ValueError("Token subject cannot be empty")

    expires_at = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": subject,
        "type": token_type,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        _get_secret_key(),
        algorithm=_get_algorithm(),
    )

def create_access_token(subject: str) -> str:
    return _create_token(
        subject,
        ACCESS_TOKEN_TYPE,
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

def create_refresh_token(subject: str) -> str:
    return _create_token(
        subject,
        REFRESH_TOKEN_TYPE,
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

def decode_token(token: str, expected_type: str | None = None) -> dict[str, Any]:
    if jwt is None:
        raise _MissingDependencyError("python-jose is required to decode JWT tokens")
    if not isinstance(token, str) or not token:
        raise ValueError("Token is required")

    try:
        payload = jwt.decode(
            token,
            _get_secret_key(),
            algorithms=[_get_algorithm()],
        )
    except Exception as exc:  # pragma: no cover - depends on JWT backend
        raise ValueError("Invalid or expired token") from exc

    if expected_type and payload.get("type") != expected_type:
        raise ValueError(f"Token type mismatch: expected {expected_type}")

    if not payload.get("sub"):
        raise ValueError("Token payload does not contain a valid subject")

    return payload

def verify_token(token: str, expected_type: str | None = None) -> dict[str, Any] | None:
    try:
        return decode_token(token, expected_type)
    except (ValueError, TypeError):
        return None

