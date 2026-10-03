#app/api/v1/sales.py

# pyright: reportMissingImports=false
from decimal import Decimal

from fastapi import APIRouter, Depends, Query  # pyright: ignore[reportMissingImports]
from pydantic import BaseModel, Field  # pyright: ignore[reportMissingImports]
from app.api.dependencies import get_current_user  # pyright: ignore[reportMissingImports]

router = APIRouter()


class SaleItem(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(ge=0)


class SaleCreate(BaseModel):
    customer_id: int = Field(gt=0)
    items: list[SaleItem] = Field(..., min_items=1)


class SaleUpdate(BaseModel):
    customer_id: int | None = Field(default=None, gt=0)
    items: list[SaleItem] | None = Field(default=None, min_items=1)


class PaymentCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    payment_method: str = Field(min_length=1, max_length=50)


@router.get("/")
def get_sales(
    current_user=Depends(get_current_user),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
):
    _ = current_user
    return {"items": [], "total": 0, "skip": skip, "limit": limit}

@router.post("/")
def create_sale(
    sale: SaleCreate,
    current_user=Depends(get_current_user),
):
    _ = current_user
    return {"message": "Sale created", "sale": sale.dict()}

@router.get("/{sale_id}")
def get_sale(
    sale_id: int,
    current_user=Depends(get_current_user),
):
    _ = current_user
    _ = sale_id
    return {"id": sale_id}

@router.put("/{sale_id}")
def update_sale(
    sale_id: int,
    sale: SaleUpdate,
    current_user=Depends(get_current_user),
):
    _ = current_user
    return {"message": "Sale updated", "id": sale_id, "updates": sale.dict(exclude_unset=True)}

@router.post("/{sale_id}/payment")
def create_payment(
    sale_id: int,
    payment: PaymentCreate,
    current_user=Depends(get_current_user),
):
    _ = current_user
    return {
        "message": "Payment recorded",
        "sale_id": sale_id,
        "amount": payment.amount,
        "payment_method": payment.payment_method,
    }

@router.get("/{sale_id}/invoice")
def get_invoice(
    sale_id: int,
    current_user=Depends(get_current_user),
):
    _ = sale_id
    _ = current_user
    return {
        "message": "Invoice",
        "sale_id": sale_id,
    }
