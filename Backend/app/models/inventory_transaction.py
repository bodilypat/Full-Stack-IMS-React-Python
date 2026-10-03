#app/models/inventory_transaction.py
# pyright: reportMissingImports=false

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class InventoryTransactionType(str, Enum):
    STOCK_IN = "stock_in"
    STOCK_OUT = "stock_out"
    ADJUSTMENT = "adjustment"
    TRANSFER = "transfer"


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    type: Mapped[InventoryTransactionType] = (
        mapped_column(
            SQLEnum(
                InventoryTransactionType,
                name="inventory_transaction_type",
                values_callable=lambda enum: [member.value for member in enum],
                validate_strings=True,
            ),
            nullable=False,
        )
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    reference: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    product = relationship(
        "Product",
        back_populates="inventory_transactions",
    )
