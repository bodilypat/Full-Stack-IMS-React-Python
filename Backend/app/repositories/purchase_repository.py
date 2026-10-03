#app/repositories/purchase_repository.py
# pyright: reportMissingImports=false

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem

def get_by_id(
    db: Session,
    purchase_id: int,
) -> Purchase | None:
    return db.get(Purchase, purchase_id)


def get_all(
    db: Session,
    offset: int = 0,
    limit: int = 20,
) -> list[Purchase]:
    statement = (
        select(Purchase)
        .order_by(Purchase.id.desc())
        .offset(offset)
        .limit(limit)
    )

    return db.scalars(statement).all()

def create(
    db: Session,
    purchase: Purchase,
) -> Purchase:
    db.add(purchase)
    db.flush()
    db.refresh(purchase)

    return purchase

def create_item(
    db: Session,
    item: PurchaseItem,
) -> PurchaseItem:
    db.add(item)
    db.flush()
    db.refresh(item)

    return item

def update(
    db: Session,
    purchase: Purchase,
) -> Purchase:
    db.add(purchase)
    db.flush()
    db.refresh(purchase)

    return purchase

def delete(
    db: Session,
    purchase: Purchase,
) -> None:
    db.delete(purchase)
    db.flush()
