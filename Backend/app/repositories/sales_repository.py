#app/repositories/sales_repository.py
# pyright: reportMissingImports=false

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sale import Sale
from app.models.sale_item import SaleItem


def get_by_id(
    db: Session,
    sale_id: int,
) -> Sale | None:
    return db.get(Sale, sale_id)


def get_all(
    db: Session,
    offset: int = 0,
    limit: int = 20,
) -> list[Sale]:
    statement = (
        select(Sale)
        .offset(offset)
        .limit(limit)
        .order_by(Sale.id.desc())
    )

    return list(db.scalars(statement).all())


def create(
    db: Session,
    sale: Sale,
) -> Sale:
    db.add(sale)
    db.flush()
    db.refresh(sale)

    return sale


def create_item(
    db: Session,
    item: SaleItem,
) -> SaleItem:
    db.add(item)
    db.flush()
    db.refresh(item)

    return item


def get_items_by_sale_id(
    db: Session,
    sale_id: int,
) -> list[SaleItem]:
    statement = (
        select(SaleItem)
        .where(SaleItem.sale_id == sale_id)
        .order_by(SaleItem.id)
    )

    return list(db.scalars(statement).all())


def update(
    db: Session,
    sale: Sale,
) -> Sale:
    db.add(sale)
    db.flush()
    db.refresh(sale)

    return sale


def delete(
    db: Session,
    sale: Sale,
) -> None:
    db.delete(sale)
    db.flush()
