# app/services/sales_service.py
# pyright: reportMissingImports=false

from importlib import import_module
from pkgutil import iter_modules
from typing import Any

from sqlalchemy.orm import Session

from app.core.exceptions import (
    InsufficientStockException,
    NotFoundException,
)
from app.schemas.sale import (
    SaleCreate,
    SaleUpdate,
)


def _model(*names: str) -> Any:
    package = import_module("app.models")
    modules = [package]
    for module in iter_modules(getattr(package, "__path__", [])):
        try:
            modules.append(import_module(f"app.models.{module.name}"))
        except ImportError:
            continue
    for name in names:
        for module in modules:
            model = getattr(module, name, None)
            if model is not None:
                return model
    raise NotFoundException(f"Required model {names[0]} was not found.")


def _columns(model: Any) -> set[str]:
    return {column.key for column in model.__table__.columns}


def _make(model: Any, **values: Any) -> Any:
    columns = _columns(model)
    return model(**{key: value for key, value in values.items() if key in columns})


def _get(value: Any, *names: str, default: Any = None) -> Any:
    for name in names:
        if isinstance(value, dict) and name in value:
            return value[name]
        if hasattr(value, name):
            return getattr(value, name)
    return default


def _stock_field(product: Any) -> str | None:
    return next(
        (name for name in ("quantity", "stock", "stock_quantity", "current_stock")
         if name in _columns(type(product))),
        None,
    )


def _rollback(db: Session) -> None:
    try:
        db.rollback()
    except Exception:
        pass

def _validate_db_session(db: Session | None) -> None:
    if db is None:
        raise NotFoundException("Database session is required.")

def create_sale(
    db: Session,
    data: SaleCreate,
    user_id: int,
):
    _validate_db_session(db)
    if user_id <= 0:
        raise NotFoundException("User not found.")

    items = getattr(data, "items", None)
    if items is None or len(items) == 0:
        raise InsufficientStockException("Sale must contain at least one item.")

    Sale = _model("Sale")
    SaleItem = _model("SaleItem", "SalesItem")
    Product = _model("Product")
    InventoryTransaction = _model("InventoryTransaction", "StockTransaction")

    customer_id = _get(data, "customer_id")
    if customer_id is not None:
        Customer = _model("Customer")
        if db.query(Customer).filter(Customer.id == customer_id).first() is None:
            raise NotFoundException("Customer not found.")

    prepared: list[tuple[Any, int, float]] = []
    total = 0.0
    for item in items:
        product_id = _get(item, "product_id")
        quantity = _get(item, "quantity")
        if product_id is None or not isinstance(quantity, int) or quantity <= 0:
            raise InsufficientStockException("Each item must have a product and a positive quantity.")
        product = db.query(Product).filter(Product.id == product_id).with_for_update().first()
        if product is None:
            raise NotFoundException(f"Product {product_id} not found.")
        stock_field = _stock_field(product)
        if stock_field is None or getattr(product, stock_field) < quantity:
            raise InsufficientStockException(f"Insufficient stock for product {product_id}.")
        price = _get(product, "selling_price", "sale_price", "price", "unit_price")
        if price is None or price < 0:
            raise InsufficientStockException(f"Invalid price for product {product_id}.")
        price = float(price)
        total += price * quantity
        prepared.append((product, quantity, price))

    try:
        sale = _make(
            Sale,
            customer_id=customer_id,
            user_id=user_id,
            total=total,
            total_amount=total,
            status="completed",
        )
        db.add(sale)
        db.flush()
        for product, quantity, price in prepared:
            db.add(_make(
                SaleItem,
                sale_id=sale.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=price,
                price=price,
                subtotal=price * quantity,
                total=price * quantity,
            ))
            field = _stock_field(product)
            setattr(product, field, getattr(product, field) - quantity)
            db.add(_make(
                InventoryTransaction,
                product_id=product.id,
                user_id=user_id,
                transaction_type="sale",
                type="sale",
                quantity=quantity,
                change=-quantity,
                reference_id=sale.id,
                reference_type="sale",
                notes=f"Sale #{sale.id}",
            ))
        db.commit()
        db.refresh(sale)
        return sale
    except Exception:
        _rollback(db)
        raise

def get_sale(
    db: Session,
    sale_id: int,
):
    _validate_db_session(db)
    if sale_id <= 0:
        raise NotFoundException("Sale not found.")

    Sale = _model("Sale")
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if sale is None:
        raise NotFoundException("Sale not found.")
    return sale

def get_sales(
    db: Session,
    page: int = 1,
    limit: int = 20,
):
    _validate_db_session(db)
    if page < 1:
        raise NotFoundException("Page must be greater than or equal to 1.")
    if limit < 1:
        raise InsufficientStockException("Limit must be greater than or equal to 1.")

    Sale = _model("Sale")
    return (
        db.query(Sale)
        .order_by(Sale.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

def update_sale(
    db: Session,
    sale_id: int,
    data: SaleUpdate,
):
    _validate_db_session(db)
    if sale_id <= 0:
        raise NotFoundException("Sale not found.")
    if data is None:
        raise NotFoundException("Sale update payload is required.")

    sale = get_sale(db, sale_id)
    values = (
        data.model_dump(exclude_unset=True)
        if hasattr(data, "model_dump")
        else data.dict(exclude_unset=True)
    )
    columns = _columns(type(sale))
    for key, value in values.items():
        if key in columns and key not in {"id", "user_id", "total", "total_amount"}:
            setattr(sale, key, value)
    try:
        db.commit()
        db.refresh(sale)
        return sale
    except Exception:
        _rollback(db)
        raise

def cancel_sale(
    db: Session,
    sale_id: int,
):
    _validate_db_session(db)
    if sale_id <= 0:
        raise NotFoundException("Sale not found.")

    sale = get_sale(db, sale_id)
    if str(_get(sale, "status", default="")).lower() in {"cancelled", "canceled", "refunded"}:
        return sale
    SaleItem = _model("SaleItem", "SalesItem")
    Product = _model("Product")
    InventoryTransaction = _model("InventoryTransaction", "StockTransaction")
    try:
        items = db.query(SaleItem).filter(SaleItem.sale_id == sale_id).all()
        for item in items:
            product = (
                db.query(Product)
                .filter(Product.id == item.product_id)
                .with_for_update()
                .first()
            )
            if product is None:
                raise NotFoundException(f"Product {item.product_id} not found.")
            field = _stock_field(product)
            if field is None:
                raise InsufficientStockException("Product stock field was not found.")
            quantity = _get(item, "quantity", default=0)
            setattr(product, field, getattr(product, field) + quantity)
            db.add(_make(
                InventoryTransaction,
                product_id=product.id,
                user_id=_get(sale, "user_id"),
                transaction_type="sale_cancellation",
                type="sale_cancellation",
                quantity=quantity,
                change=quantity,
                reference_id=sale.id,
                reference_type="sale",
                notes=f"Cancellation of sale #{sale.id}",
            ))
        sale_columns = _columns(type(sale))
        if "status" in sale_columns:
            sale.status = "cancelled"
        elif "is_cancelled" in sale_columns:
            sale.is_cancelled = True
        db.commit()
        db.refresh(sale)
        return sale
    except Exception:
        _rollback(db)
        raise
