#app/schemas/sale.py
# pyright: reportMissingImports=false

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SaleItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(ge=0, max_digits=12, decimal_places=2)


class SaleCreate(BaseModel):
    customer_id: int | None = Field(default=None, gt=0)
    items: list[SaleItemCreate] = Field(min_length=1)
    notes: str | None = Field(default=None, max_length=1000)


class SaleUpdate(BaseModel):
    customer_id: int | None = Field(default=None, gt=0)
    notes: str | None = Field(default=None, max_length=1000)


class SaleItemResponse(SaleItemCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class SaleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int | None
    status: str
    total: Decimal
    notes: str | None
    created_at: datetime
    items: list[SaleItemResponse]
