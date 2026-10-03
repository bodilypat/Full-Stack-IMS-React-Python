#app/utils/formatters.py

from decimal import Decimal, ROUND_HALF_UP


def format_currency(
    amount: Decimal | float | int,
    currency: str = "$",
) -> str:
    value = Decimal(str(amount)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    return f"{currency}{value:,.2f}"


def format_quantity(
    quantity: int,
) -> str:
    return f"{quantity:,}"


def format_percentage(
    value: Decimal | float,
) -> str:
    rounded_value = Decimal(str(value)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )
    return f"{rounded_value:.2f}%"


def format_sku(
    sku: str,
) -> str:
    return sku.strip().upper()

