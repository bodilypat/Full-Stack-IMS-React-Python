#app/services/customer_service.py
# pyright: reportMissingImports=false

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.sale import Sale

def get_customers(
    db: Session,
    skip: int = 0,
    limit: int = 20,
):
    return db.query(Customer).offset(skip).limit(limit).all()

def get_customer(
    db: Session,
    customer_id: int,
):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def create_customer(
    db: Session,
    data,
):
    db_customer = Customer(**data)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(
    db: Session,
    customer_id: int,
    data,
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return None

    for key, value in data.items():
        if value is not None:
            setattr(customer, key, value)

    db.commit()
    db.refresh(customer)
    return customer

def delete_customer(
    db: Session,
    customer_id: int,
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return None

    # Keep historical sales intact; a customer with sales cannot be removed.
    if db.query(Sale.id).filter(Sale.customer_id == customer_id).first():
        raise ValueError("Cannot delete a customer with existing sales.")

    db.delete(customer)
    db.commit()
    return customer

def get_customer_sales(
    db: Session,
    customer_id: int,
):
    return db.query(Sale).filter(Sale.customer_id == customer_id).all()
