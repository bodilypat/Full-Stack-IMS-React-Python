#app/repositories/customer_repository.py
# pyright: reportMissingImports=false

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer

def get_by_id(
    db: Session,
    customer_id: int,
) -> Customer | None:
    return db.get(Customer, customer_id)

def get_by_email(
    db: Session,
    email: str,
) -> Customer | None:
    statement = select(Customer).where(
        Customer.email == email
    )

    return db.scalar(statement)

def get_all(
    db: Session,
    offset: int = 0,
    limit: int = 20,
) -> list[Customer]:
    statement = (
        select(Customer)
        .order_by(Customer.id.desc())
        .offset(offset)
        .limit(limit)
    )

    return list(db.scalars(statement).all())

def create(
    db: Session,
    customer: Customer,
) -> Customer:
    db.add(customer)
    db.flush()
    db.refresh(customer)

    return customer

def update(
    db: Session,
    customer: Customer,
) -> Customer:
    db.add(customer)
    db.flush()
    db.refresh(customer)

    return customer

def delete(
    db: Session,
    customer: Customer,
) -> None:
    db.delete(customer)
    db.flush()
