# app/repositories/supplier_repository.py
# pyright: reportMissingImports=false

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.supplier import Supplier


def get_by_id(
    db: Session,
    supplier_id: int,
) -> Supplier | None:
    return db.get(Supplier, supplier_id)


def get_all(
    db: Session,
    offset: int = 0,
    limit: int = 20,
) -> list[Supplier]:
    if offset < 0:
        raise ValueError("offset must be non-negative")
    if limit < 0:
        raise ValueError("limit must be non-negative")

    statement = (
        select(Supplier)
        .order_by(Supplier.id.desc())
        .offset(offset)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


def create(
    db: Session,
    supplier: Supplier,
) -> Supplier:
    db.add(supplier)
    db.flush()
    db.refresh(supplier)

    return supplier


def update(
    db: Session,
    supplier: Supplier,
) -> Supplier:
    db.add(supplier)
    db.flush()
    db.refresh(supplier)

    return supplier


def delete(
    db: Session,
    supplier: Supplier,
) -> None:
    db.delete(supplier)
    db.flush()
