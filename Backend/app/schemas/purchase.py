#app/schemas/purchase.py 

from datetime import datetime
from decimal import Decimal

# pyright: reportMissingImports=false
from pydantic import BaseModel, ConfigDict, Field


class PurchaseItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    unit_cost: Decimal = Field(ge=0)


class PurchaseCreate(BaseModel):
    supplier_id: int = Field(gt=0)
    items: list[PurchaseItemCreate] = Field(min_length=1)
    notes: str | None = None


class PurchaseUpdate(BaseModel):
    supplier_id: int | None = Field(default=None, gt=0)
    notes: str | None = None


class ReceivePurchaseRequest(BaseModel):
    items: list[PurchaseItemCreate] = Field(min_length=1)


class PurchaseItemResponse(PurchaseItemCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)


class PurchaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    supplier_id: int = Field(gt=0)
    status: str
    total: Decimal = Field(ge=0)
    notes: str | None
    created_at: datetime
    items: list[PurchaseItemResponse]
