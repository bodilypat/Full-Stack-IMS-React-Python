# app/repositories/inventory_repository.py
# pyright: reportMissingImports=false

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.inventory_transaction import (
    InventoryTransaction,
)


def _normalize_pagination(
    offset: int,
    limit: int,
) -> tuple[int, int]:
    offset = max(offset, 0)
    limit = max(limit, 0)
    return offset, limit


def get_by_product_id(
    db: Session,
    product_id: int,
) -> Inventory | None:
    statement = (
        select(Inventory)
        .where(Inventory.product_id == product_id)
        .order_by(Inventory.id.desc())
        .limit(1)
    )

    return db.scalar(statement)


def get_all(
    db: Session,
    product_id: int | None = None,
    offset: int = 0,
    limit: int = 20,
) -> list[Inventory]:
    offset, limit = _normalize_pagination(offset, limit)

    if limit == 0:
        return []

    statement = select(Inventory)

    if product_id is not None:
        statement = statement.where(Inventory.product_id == product_id)

    statement = (
        statement
        .order_by(Inventory.id.desc())
        .offset(offset)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


def create(
    db: Session,
    inventory: Inventory,
) -> Inventory:
    db.add(inventory)
    db.flush()
    db.refresh(inventory)

    return inventory


def update(
    db: Session,
    inventory: Inventory,
) -> Inventory:
    db.add(inventory)
    db.flush()
    db.refresh(inventory)

    return inventory


def create_transaction(
    db: Session,
    transaction: InventoryTransaction,
) -> InventoryTransaction:
    db.add(transaction)
    db.flush()
    db.refresh(transaction)

    return transaction


def get_transactions(
    db: Session,
    product_id: int | None = None,
    offset: int = 0,
    limit: int = 50,
) -> list[InventoryTransaction]:
    offset, limit = _normalize_pagination(offset, limit)

    if limit == 0:
        return []

    statement = select(InventoryTransaction)

    if product_id is not None:
        statement = statement.where(
            InventoryTransaction.product_id == product_id
        )

    statement = (
        statement
        .order_by(InventoryTransaction.id.desc())
        .offset(offset)
        .limit(limit)
    )

    return list(db.scalars(statement).all())
