# app/services/inventory_service.py

from sqlalchemy.orm import Session  # type: ignore[reportMissingImports]

from ..core.exceptions import (  # type: ignore[reportMissingImports]
    InsufficientStockException,
    NotFoundException,
)
from ..models.product import Product  # type: ignore[reportMissingImports]
from ..models.user import User  # type: ignore[reportMissingImports]

def _get_product_stock(product: Product) -> int:
    for attr_name in ("stock", "quantity", "stock_quantity", "available_quantity"):
        if hasattr(product, attr_name):
            value = getattr(product, attr_name)
            if value is not None:
                return int(value)
    raise AttributeError("Product model does not define a stock field")

def _set_product_stock(product: Product, value: int) -> None:
    for attr_name in ("stock", "quantity", "stock_quantity", "available_quantity"):
        if hasattr(product, attr_name):
            setattr(product, attr_name, value)
            return
    raise AttributeError("Product model does not define a stock field")

def stock_in(
    db: Session,
    product_id: int,
    quantity: int,
    user_id: int,
    reference: str | None = None,
    notes: str | None = None,
):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise NotFoundException(f"User with id {user_id} was not found")

    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise NotFoundException(f"Product with id {product_id} was not found")

    current_stock = _get_product_stock(product)
    new_stock = current_stock + quantity
    _set_product_stock(product, new_stock)

    if reference is not None and hasattr(product, "reference"):
        product.reference = reference
    if notes is not None and hasattr(product, "notes"):
        product.notes = notes

    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def stock_out(
    db: Session,
    product_id: int,
    quantity: int,
    user_id: int,
    reference: str | None = None,
    notes: str | None = None,
):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise NotFoundException(f"User with id {user_id} was not found")

    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise NotFoundException(f"Product with id {product_id} was not found")

    current_stock = _get_product_stock(product)
    if current_stock < quantity:
        raise InsufficientStockException(
            f"Not enough stock for product {product_id}. Available: {current_stock}, requested: {quantity}"
        )

    new_stock = current_stock - quantity
    _set_product_stock(product, new_stock)

    if reference is not None and hasattr(product, "reference"):
        product.reference = reference
    if notes is not None and hasattr(product, "notes"):
        product.notes = notes

    db.add(product)
    db.commit()
    db.refresh(product)
    return product

    