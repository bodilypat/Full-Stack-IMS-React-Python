"""Utility helpers for the application."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any, Iterable


def to_snake_case(value: str) -> str:
    """Convert a CamelCase or PascalCase string to snake_case."""
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value)
    return value.strip("_").lower()


def slugify(value: str, *, separator: str = "-") -> str:
    """Create a URL-friendly slug from the provided text."""
    normalized = to_snake_case(value)
    return normalized.replace("_", separator)


def ensure_list(value: Any) -> list[Any]:
    """Return a list for scalar or list-like inputs."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, set):
        return list(value)
    return [value]


def parse_bool(value: Any, default: bool = False) -> bool:
    """Safely parse truthy/falsy values from strings or booleans."""
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "y", "on"}:
            return True
        if normalized in {"0", "false", "no", "n", "off", ""}:
            return False
    return default


def safe_int(value: Any, default: int = 0) -> int:
    """Convert a value to int, returning a default if conversion fails."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    """Convert a value to float, returning a default if conversion fails."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def normalize_dict(data: dict[str, Any] | None, *, default: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return a dictionary and ensure None values are converted to an empty dict."""
    if not isinstance(data, dict):
        return {} if default is None else default
    return data


def utc_now() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(timezone.utc)


def isoformat_utc(value: datetime | None = None) -> str:
    """Return an ISO 8601 UTC timestamp string."""
    timestamp = value or utc_now()
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    return timestamp.astimezone(timezone.utc).isoformat()


def dump_json(data: Any, *, pretty: bool = False, default: Any = None) -> str:
    """Serialize Python objects to JSON."""
    indent = 2 if pretty else None
    return json.dumps(data, indent=indent, default=default)


def flatten(items: Iterable[Iterable[Any]]) -> list[Any]:
    """Flatten a nested iterable into a single list."""
    return [item for sublist in items for item in sublist]


__all__ = [
    "to_snake_case",
    "slugify",
    "ensure_list",
    "parse_bool",
    "safe_int",
    "safe_float",
    "normalize_dict",
    "utc_now",
    "isoformat_utc",
    "dump_json",
    "flatten",
]

