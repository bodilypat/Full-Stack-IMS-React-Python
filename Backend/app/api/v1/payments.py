"""API endpoints for recording and managing inventory payments."""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.payment import Payment

router = APIRouter(prefix="/payments", tags=["Payments"])


class PaymentCreate(BaseModel):
	sale_id: Optional[int] = Field(default=None, gt=0)
	amount: float = Field(gt=0)
	payment_method: str = Field(min_length=1, max_length=50)
	payment_date: Optional[datetime] = None
	reference: Optional[str] = Field(default=None, max_length=100)


class PaymentUpdate(BaseModel):
	amount: Optional[float] = Field(default=None, gt=0)
	payment_method: Optional[str] = Field(default=None, min_length=1, max_length=50)
	payment_date: Optional[datetime] = None
	reference: Optional[str] = Field(default=None, max_length=100)
	status: Optional[str] = Field(default=None, max_length=30)


class PaymentResponse(BaseModel):
	id: int
	sale_id: Optional[int] = None
	amount: float
	payment_method: str
	payment_date: Optional[datetime] = None
	reference: Optional[str] = None
	status: Optional[str] = None

	class Config:
		orm_mode = True


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
	payment = Payment(**payload.dict(exclude_unset=True))
	db.add(payment)
	db.commit()
	db.refresh(payment)
	return payment


@router.get("", response_model=list[PaymentResponse])
def list_payments(
	sale_id: Optional[int] = Query(default=None, gt=0),
	payment_status: Optional[str] = Query(default=None, alias="status"),
	skip: int = Query(default=0, ge=0),
	limit: int = Query(default=100, ge=1, le=500),
	db: Session = Depends(get_db),
):
	query = db.query(Payment)
	if sale_id is not None:
		query = query.filter(Payment.sale_id == sale_id)
	if payment_status:
		query = query.filter(Payment.status == payment_status)
	return query.order_by(Payment.id.desc()).offset(skip).limit(limit).all()


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
	payment = db.query(Payment).filter(Payment.id == payment_id).first()
	if payment is None:
		raise HTTPException(status_code=404, detail="Payment not found")
	return payment


@router.patch("/{payment_id}", response_model=PaymentResponse)
def update_payment(
	payment_id: int, payload: PaymentUpdate, db: Session = Depends(get_db)
):
	payment = db.query(Payment).filter(Payment.id == payment_id).first()
	if payment is None:
		raise HTTPException(status_code=404, detail="Payment not found")
	for field, value in payload.dict(exclude_unset=True).items():
		setattr(payment, field, value)
	db.commit()
	db.refresh(payment)
	return payment


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
	payment = db.query(Payment).filter(Payment.id == payment_id).first()
	if payment is None:
		raise HTTPException(status_code=404, detail="Payment not found")
	db.delete(payment)
	db.commit()

