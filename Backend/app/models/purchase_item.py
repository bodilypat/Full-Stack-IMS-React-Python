#app/models/purchase_item.py
# pyright: reportMissingImports=false

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric  # type: ignore[import-not-found]
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore[import-not-found]

from app.db.base import Base  # type: ignore[import-not-found]

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.purchase import Purchase


class PurchaseItem(Base):
    __tablename__ = "purchase_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_purchase_items_quantity_positive"),
        CheckConstraint("unit_cost >= 0", name="ck_purchase_items_unit_cost_nonnegative"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    purchase_id: Mapped[int] = mapped_column(
        ForeignKey("purchases.id"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    unit_cost: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    purchase: Mapped["Purchase"] = relationship(
        "Purchase",
        back_populates="items",
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="purchase_items",
    )
