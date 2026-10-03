#app/models/purchase.py

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import (  # type: ignore
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore

from app.db.base import Base  # type: ignore

if TYPE_CHECKING:
    from app.models.purchase_item import PurchaseItem  # type: ignore[reportMissingImports]
    from app.models.supplier import Supplier  # type: ignore[reportMissingImports]


class PurchaseStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PARTIALLY_RECEIVED = "partially_received"
    RECEIVED = "received"
    CANCELLED = "cancelled"


class Purchase(Base):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id"),
        nullable=False,
        index=True,
    )

    status: Mapped[PurchaseStatus] = mapped_column(
        SQLEnum(
            PurchaseStatus,
            name="purchase_status",
            values_callable=lambda enum: [status.value for status in enum],
            validate_strings=True,
        ),
        default=PurchaseStatus.DRAFT,
        nullable=False,
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    supplier: Mapped["Supplier"] = relationship(
        "Supplier",
        back_populates="purchases",
    )

    items: Mapped[list["PurchaseItem"]] = relationship(
        "PurchaseItem",
        back_populates="purchase",
        cascade="all, delete-orphan",
    )
