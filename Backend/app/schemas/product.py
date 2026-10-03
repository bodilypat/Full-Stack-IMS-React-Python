# app/schemas/product.py
# pyright: reportMissingImports=false

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    sku: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=200)
    category_id: int = Field(gt=0)
    cost_price: Decimal = Field(ge=0)
    selling_price: Decimal = Field(ge=0)


class ProductCreate(ProductBase):
    supplier_id: int | None = Field(default=None, gt=0)
    reorder_level: int = Field(default=0, ge=0)
    description: str | None = None


class ProductUpdate(ProductBase):
    sku: str | None = Field(default=None, min_length=1, max_length=50)
    name: str | None = Field(default=None, min_length=1, max_length=200)
    category_id: int | None = Field(default=None, gt=0)
    cost_price: Decimal | None = Field(default=None, ge=0)
    selling_price: Decimal | None = Field(default=None, ge=0)
    supplier_id: int | None = Field(default=None, gt=0)
    reorder_level: int | None = Field(default=None, ge=0)
    description: str | None = None
    is_active: bool | None = None


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    id: int = Field(gt=0)
    supplier_id: int | None
    quantity: int = Field(ge=0)
    reorder_level: int = Field(ge=0)
    description: str | None
    is_active: bool
    created_at: datetime
