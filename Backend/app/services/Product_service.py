# app/services/product_service.py

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

try:
    from sqlalchemy.orm import Session as SQLAlchemySession  # pyright: ignore[reportMissingImports]
except ImportError:  # pragma: no cover
    SQLAlchemySession = Any  # type: ignore[assignment]

try:
    from app.core.exceptions import (  # pyright: ignore[reportMissingImports]
        ConflictException,
        NotFoundException,
    )
except ImportError:  # pragma: no cover
    class ConflictException(Exception):
        """Raised when a resource conflicts with an existing one."""

    class NotFoundException(Exception):
        """Raised when a resource cannot be found."""

Session = SQLAlchemySession

try:
    from app.models.product import Product  # pyright: ignore[reportMissingImports]
except ImportError:  # pragma: no cover
    Product = None

try:
    from sqlalchemy.exc import IntegrityError  # pyright: ignore[reportMissingImports]
except ImportError:  # pragma: no cover
    class IntegrityError(Exception):
        """Fallback when SQLAlchemy is not installed."""


def _product_model():
    if Product is None:
        raise RuntimeError("The Product model is not available")
    return Product


def _payload(data) -> dict[str, Any]:
    if isinstance(data, Mapping):
        return dict(data)
    if hasattr(data, "model_dump"):
        return data.model_dump(exclude_unset=True)
    if hasattr(data, "dict"):
        return data.dict(exclude_unset=True)
    raise ValueError("Product data must be a mapping or schema")


def _product_fields(model) -> set[str]:
    table = getattr(model, "__table__", None)
    if table is not None:
        return set(table.columns.keys())
    return set()


def _ensure_unique_sku(db, sku, exclude_id=None) -> None:
    if not sku:
        return
    model = _product_model()
    query = db.query(model).filter(model.sku == sku)
    if exclude_id is not None:
        query = query.filter(model.id != exclude_id)
    if query.first() is not None:
        raise ConflictException("Product with this SKU already exists")


def get_products(
    db: "Session",
    skip: int = 0,
    limit: int = 20,
):
    if skip < 0:
        raise ValueError("skip cannot be negative")
    if limit <= 0:
        raise ValueError("limit must be greater than zero")

    return db.query(_product_model()).offset(skip).limit(limit).all()

def get_product(
    db: "Session",
    product_id: int,
):
    if product_id is None or product_id <= 0:
        raise NotFoundException("Product not found")

    product = db.query(_product_model()).filter(_product_model().id == product_id).first()
    if product is None:
        raise NotFoundException("Product not found")
    return product

def create_product(
    db: "Session",
    data,
):
    if not data:
        raise ValueError("Product data is required")

    model = _product_model()
    values = _payload(data)
    allowed = _product_fields(model)
    if allowed:
        values = {key: value for key, value in values.items() if key in allowed}
    values.pop("id", None)
    if not values:
        raise ValueError("No valid product fields were provided")

    _ensure_unique_sku(db, values.get("sku"))
    product = model(**values)
    try:
        db.add(product)
        db.commit()
        db.refresh(product)
    except IntegrityError as exc:
        db.rollback()
        if values.get("sku"):
            raise ConflictException("Product with this SKU already exists") from exc
        raise
    except Exception:
        db.rollback()
        raise
    return product

def update_product(
    db: "Session",
    product_id: int,
    data,
):
    if product_id is None or product_id <= 0:
        raise NotFoundException("Product not found")
    if not data:
        raise ValueError("Product data is required")

    product = get_product(db, product_id)
    values = _payload(data)
    allowed = _product_fields(_product_model())
    if allowed:
        values = {key: value for key, value in values.items() if key in allowed}
    values.pop("id", None)
    if not values:
        raise ValueError("No valid product fields were provided")

    if "sku" in values:
        _ensure_unique_sku(db, values["sku"], exclude_id=product_id)
    try:
        for key, value in values.items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
    except IntegrityError as exc:
        db.rollback()
        if values.get("sku"):
            raise ConflictException("Product with this SKU already exists") from exc
        raise
    except Exception:
        db.rollback()
        raise
    return product

def delete_product(
    db: "Session",
    product_id: int,
):
    if product_id is None or product_id <= 0:
        raise NotFoundException("Product not found")

    product = get_product(db, product_id)
    try:
        db.delete(product)
        db.commit()
    except Exception:
        db.rollback()
        raise
    return True
