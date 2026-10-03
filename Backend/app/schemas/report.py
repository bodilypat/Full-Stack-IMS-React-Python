# app/schemas/report.py

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field, root_validator  # type: ignore[import-not-found]

class ReportDateRange(BaseModel):
    start_date: date
    end_date: date

    @root_validator
    def validate_date_range(cls, values):
        start_date = values.get("start_date")
        end_date = values.get("end_date")
        if start_date is not None and end_date is not None and start_date > end_date:
            raise ValueError("start_date must be on or before end_date")
        return values

class SalesReportRow(BaseModel):
    date: date
    orders: int = Field(ge=0)
    quantity: int = Field(ge=0)
    revenue: Decimal = Field(ge=0)

class PurchaseReportRow(BaseModel):
    date: date
    purchases: int = Field(ge=0)
    quantity: int = Field(ge=0)
    total: Decimal = Field(ge=0)

class InventoryReportRow(BaseModel):
    product_id: int = Field(gt=0)
    product_name: str = Field(min_length=1)
    sku: str = Field(min_length=1)
    quantity: int = Field(ge=0)
    inventory_value: Decimal = Field(ge=0)

class SalesReportResponse(ReportDateRange):
    total_sales: Decimal = Field(ge=0)
    rows: List[SalesReportRow]

class PurchaseReportResponse(ReportDateRange):
    total_purchases: Decimal = Field(ge=0)
    rows: List[PurchaseReportRow]

class InventoryReportResponse(BaseModel):
    as_of_date: date
    total_inventory_value: Decimal = Field(ge=0)
    rows: List[InventoryReportRow]

