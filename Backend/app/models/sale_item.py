#app/models/sale_item.py

from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric  # type: ignore
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore

from app.db.base import Base  # type: ignore


class SaleItem(Base):
    __tablename__ = "sale_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_sale_items_quantity_positive"),
        CheckConstraint("unit_price >= 0", name="ck_sale_items_unit_price_nonnegative"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    sale_id: Mapped[int] = mapped_column(
        ForeignKey("sales.id"),
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

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    sale = relationship(
        "Sale",
        back_populates="items",
    )

    product = relationship(
        "Product",
        back_populates="sale_items",
    )
