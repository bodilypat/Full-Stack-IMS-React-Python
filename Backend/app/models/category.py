# app/models/category.py
# pyright: reportMissingImports=false

from typing import TYPE_CHECKING

from sqlalchemy import String, Text  # type: ignore[import-not-found]
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore[import-not-found]

from app.db.base import Base  # type: ignore[import-not-found]

if TYPE_CHECKING:
    from app.models.product import Product


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="category",
    )

