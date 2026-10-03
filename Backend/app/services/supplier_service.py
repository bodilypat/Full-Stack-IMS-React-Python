#app/services/supplier_service.py

# pyright: reportMissingImports=false
from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.models.supplier import Supplier
from app.models.product import Product
from app.models.purchase import Purchase

def get_suppliers(
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> list[Supplier]:
    return db.query(Supplier).offset(skip).limit(limit).all()

def get_supplier(
    db: Session,
    supplier_id: int,
) -> Supplier | None:
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()

def create_supplier(
    db: Session,
    data: dict[str, Any],
) -> Supplier:
    supplier = Supplier(**data)
    db.add(supplier)
    try:
        db.commit()
        db.refresh(supplier)
    except Exception:
        db.rollback()
        raise
    return supplier

def update_supplier(
    db: Session,
    supplier_id: int,
    data: dict[str, Any],
) -> Supplier | None:
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if supplier is None:
        return None

    changed = False
    for key, value in data.items():
        # The primary key is managed by the database, not update payloads.
        if key != "id" and hasattr(supplier, key):
            setattr(supplier, key, value)
            changed = True

    if changed:
        try:
            db.commit()
            db.refresh(supplier)
        except Exception:
            db.rollback()
            raise
    return supplier

def delete_supplier(
    db: Session,
    supplier_id: int,
) -> Supplier | None:
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if supplier is None:
        return None

    db.delete(supplier)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    return supplier

def get_supplier_products(
    db: Session,
    supplier_id: int,
) -> list[Product]:
    return db.query(Product).filter(Product.supplier_id == supplier_id).all()


def get_purchase_history(
    db: Session,
    supplier_id: int,
) -> list[Purchase]:
    return db.query(Purchase).filter(Purchase.supplier_id == supplier_id).all()

