#app/utils/invoice.py

from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable


def calculate_invoice_subtotal(
    items: Iterable[dict],
) -> Decimal:
    subtotal = Decimal("0")

    for item in items:
        quantity = Decimal(str(item["quantity"]))
        unit_price = Decimal(str(item["unit_price"]))

        subtotal += quantity * unit_price

    return subtotal


def calculate_invoice_tax(
    subtotal: Decimal,
    tax_rate: Decimal,
) -> Decimal:
    return (
        subtotal * tax_rate / Decimal("100")
    )


def calculate_invoice_total(
    subtotal: Decimal,
    tax: Decimal,
    discount: Decimal = Decimal("0"),
) -> Decimal:
    return subtotal + tax - discount


def build_invoice_summary(
    items: list[dict],
    tax_rate: Decimal = Decimal("0"),
    discount: Decimal = Decimal("0"),
) -> dict:
    subtotal = calculate_invoice_subtotal(items)

    tax = calculate_invoice_tax(
        subtotal,
        tax_rate,
    )

    total = calculate_invoice_total(
        subtotal,
        tax,
        discount,
    )

    return {
        "subtotal": subtotal,
        "tax": tax,
        "discount": discount,
        "total": total,
    }


def format_invoice_amount(
    amount: Decimal,
    currency_symbol: str = "$",
) -> str:
    """Format an amount as currency, rounded to two decimal places."""
    rounded_amount = amount.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )
    sign = "-" if rounded_amount < 0 else ""
    return f"{sign}{currency_symbol}{abs(rounded_amount):,.2f}"


def format_invoice_summary(
    summary: dict,
    currency_symbol: str = "$",
) -> str:
    """Generate a readable, consistently formatted invoice totals block."""
    labels = (
        ("subtotal", "Subtotal"),
        ("tax", "Tax"),
        ("discount", "Discount"),
        ("total", "Total"),
    )
    return "\n".join(
        f"{label}: {format_invoice_amount(summary[key], currency_symbol)}"
        for key, label in labels
    )
