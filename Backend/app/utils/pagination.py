#app/utils/pagination.py

from math import ceil
from typing import Any


def _normalize_page_and_limit(page: int, limit: int) -> tuple[int, int]:
    return max(page, 1), max(limit, 1)


def calculate_offset(
    page: int,
    limit: int,
) -> int:
    page, limit = _normalize_page_and_limit(page, limit)

    return (page - 1) * limit


def calculate_pages(
    total: int,
    limit: int,
) -> int:
    if total == 0:
        return 0

    return ceil(total / limit)


def build_pagination(
    *,
    page: int,
    limit: int,
    total: int,
) -> dict[str, Any]:
    page, limit = _normalize_page_and_limit(page, limit)
    pages = calculate_pages(total, limit)

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages,
        "has_next": page < pages,
        "has_previous": page > 1,
    }
