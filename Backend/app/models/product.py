#app/models/product.py
# pyright: reportMissingImports=false

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Numeric,
    String,
    Text,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.inventory import Inventory
    from app.models.inventory_transaction import InventoryTransaction
    from app.models.purchase_item import PurchaseItem
    from app.models.sale_item import SaleItem
    from app.models.supplier import Supplier

class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("cost_price >= 0", name="ck_products_cost_price_nonnegative"),
        CheckConstraint("selling_price >= 0", name="ck_products_selling_price_nonnegative"),
        CheckConstraint("reorder_level >= 0", name="ck_products_reorder_level_nonnegative"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    sku: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
        index=True,
    )

    supplier_id: Mapped[int | None] = mapped_column(
        ForeignKey("suppliers.id"),
        nullable=True,
        index=True,
    )

    cost_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    selling_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    reorder_level: Mapped[int] = mapped_column(
        default=0,
        server_default="0",
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=true(),
        nullable=False,
    )

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products",
    )

    supplier: Mapped["Supplier | None"] = relationship(
        "Supplier",
        back_populates="products",
    )

    inventory: Mapped["Inventory | None"] = relationship(
        "Inventory",
        back_populates="product",
        uselist=False,
        cascade="all, delete-orphan",
    )

    inventory_transactions: Mapped[list["InventoryTransaction"]] = relationship(
        "InventoryTransaction",
        back_populates="product",
    )

    purchase_items: Mapped[list["PurchaseItem"]] = relationship(
        "PurchaseItem",
        back_populates="product",
    )

    sale_items: Mapped[list["SaleItem"]] = relationship(
        "SaleItem",
        back_populates="product",
    )
