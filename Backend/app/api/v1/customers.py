#app/api/v1/customers.py

"""Customer management endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.customer import Customer

router = APIRouter(prefix="/customers", tags=["Customers"])


class CustomerCreate(BaseModel):
	name: str
	email: Optional[str] = None
	phone: Optional[str] = None
	address: Optional[str] = None


class CustomerUpdate(BaseModel):
	name: Optional[str] = None
	email: Optional[str] = None
	phone: Optional[str] = None
	address: Optional[str] = None


class CustomerResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	name: str
	email: Optional[str] = None
	phone: Optional[str] = None
	address: Optional[str] = None


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
	customer = Customer(**payload.model_dump())
	db.add(customer)
	db.commit()
	db.refresh(customer)
	return customer


@router.get("/", response_model=list[CustomerResponse])
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	if skip < 0 or limit < 1 or limit > 500:
		raise HTTPException(status_code=400, detail="Invalid pagination parameters")
	return db.query(Customer).offset(skip).limit(limit).all()


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
	customer = db.query(Customer).filter(Customer.id == customer_id).first()
	if customer is None:
		raise HTTPException(status_code=404, detail="Customer not found")
	return customer


@router.patch("/{customer_id}", response_model=CustomerResponse)
def update_customer(
	customer_id: int, payload: CustomerUpdate, db: Session = Depends(get_db)
):
	customer = db.query(Customer).filter(Customer.id == customer_id).first()
	if customer is None:
		raise HTTPException(status_code=404, detail="Customer not found")

	for field, value in payload.model_dump(exclude_unset=True).items():
		setattr(customer, field, value)
	db.commit()
	db.refresh(customer)
	return customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)) -> None:
	customer = db.query(Customer).filter(Customer.id == customer_id).first()
	if customer is None:
		raise HTTPException(status_code=404, detail="Customer not found")
	db.delete(customer)
	db.commit()

