#app/repositories/product_repository.py
# pyright: reportMissingImports=false

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product


def get_by_id(
    db: Session,
    product_id: int,
) -> Product | None:
    return db.get(Product, product_id)


def get_by_sku(
    db: Session,
    sku: str,
) -> Product | None:
    statement = select(Product).where(
        Product.sku == sku
    )

    return db.scalar(statement)


def get_all(
    db: Session,
    offset: int = 0,
    limit: int = 20,
    search: str | None = None,
) -> list[Product]:
    if offset < 0:
        raise ValueError("offset must be non-negative")
    if limit < 0:
        raise ValueError("limit must be non-negative")

    statement = select(Product)

    search = search.strip() if search else None
    if search:
        statement = statement.where(
            Product.name.ilike(f"%{search}%")
            | Product.sku.ilike(f"%{search}%")
        )

    statement = (
        statement
        .order_by(Product.id.desc())
        .offset(offset)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


def create(
    db: Session,
    product: Product,
) -> Product:
    db.add(product)
    db.flush()
    db.refresh(product)

    return product


def update(
    db: Session,
    product: Product,
) -> Product:
    db.add(product)
    db.flush()
    db.refresh(product)

    return product


def delete(
    db: Session,
    product: Product,
) -> None:
    db.delete(product)
    db.flush()
