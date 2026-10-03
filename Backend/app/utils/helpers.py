#app/utils/helpers.py

"""Utility helpers for common data normalization tasks."""

from collections.abc import Mapping
from typing import Any


def clean_string(value: str | None) -> str | None:
    """Trim whitespace and normalize empty strings to None."""
    if value is None:
        return None

    if not isinstance(value, str):
        value = str(value)

    value = value.strip()
    return value or None


def build_dict_without_none(data: Mapping[str, Any]) -> dict[str, Any]:
    """Return a copy of the mapping without keys whose value is None."""
    return {
        key: value
        for key, value in data.items()
        if value is not None
    }


def chunk_list(items: list[Any], size: int) -> list[list[Any]]:
    """Split a list into chunks of the given size."""
    if size <= 0:
        raise ValueError("Chunk size must be greater than zero")

    return [
        items[index:index + size]
        for index in range(0, len(items), size)
    ]


def safe_int(value: Any, default: int = 0) -> int:
    """Convert a value to int and return a fallback on failure."""
    if value is None:
        return default

    if isinstance(value, str):
        value = value.strip()
        if not value:
            return default

    try:
        return int(value)
    except (TypeError, ValueError):
        return default
