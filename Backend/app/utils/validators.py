#app/models/validators.py

import re
from decimal import Decimal


EMAIL_PATTERN = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)

SKU_PATTERN = re.compile(
    r"^[A-Za-z0-9_-]+$"
)


def is_valid_email(
    email: str,
) -> bool:
    return isinstance(email, str) and bool(
        EMAIL_PATTERN.fullmatch(email.strip())
    )


def is_valid_sku(
    sku: str,
) -> bool:
    return isinstance(sku, str) and bool(
        SKU_PATTERN.fullmatch(sku.strip())
    )


def is_positive_integer(
    value: int,
) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def is_non_negative_decimal(
    value: Decimal,
) -> bool:
    return isinstance(value, Decimal) and value.is_finite() and value >= Decimal("0")


def validate_date_range(
    start_date,
    end_date,
) -> bool:
    try:
        return start_date <= end_date
    except TypeError:
        return False

