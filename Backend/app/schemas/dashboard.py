#app/schemas/dashboard.py

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field  # type: ignore[reportMissingImports]


class DashboardStats(BaseModel):
    total_products: int = Field(ge=0)
    total_inventory_units: int = Field(ge=0)
    inventory_value: Decimal = Field(ge=0)
    total_sales: Decimal = Field(ge=0)
    total_purchases: Decimal = Field(ge=0)
    low_stock_count: int = Field(ge=0)


class SalesSummary(BaseModel):
    date: date
    total: Decimal = Field(ge=0)


class TopProduct(BaseModel):
    product_id: int = Field(gt=0)
    product_name: str = Field(min_length=1)
    quantity_sold: int = Field(ge=0)
    revenue: Decimal = Field(ge=0)


class DashboardResponse(BaseModel):
    stats: DashboardStats
    sales: list[SalesSummary]
    top_products: list[TopProduct]
