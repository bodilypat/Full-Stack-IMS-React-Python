#app/schemas/inventory.py

from datetime import datetime
from enum import Enum

try:
    from pydantic import BaseModel, Field  # type: ignore[import-not-found]
except ModuleNotFoundError:  # pragma: no cover
    # Compatibility with Pydantic v2+ branch where the v1 API remains available.
    from pydantic.v1 import BaseModel, Field  # type: ignore[import-not-found]


class InventoryTransactionType(str, Enum):
    STOCK_IN = "stock_in"
    STOCK_OUT = "stock_out"
    ADJUSTMENT = "adjustment"
    TRANSFER = "transfer"


class InventoryRequest(BaseModel):
    class Config:
        anystr_strip_whitespace = True


class InventoryOutput(BaseModel):
    class Config:
        orm_mode = True


class StockInRequest(InventoryRequest):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    reference: str | None = None
    notes: str | None = None


class StockOutRequest(InventoryRequest):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    reference: str | None = None
    notes: str | None = None


class StockAdjustmentRequest(InventoryRequest):
    product_id: int = Field(gt=0)
    quantity: int
    reason: str = Field(min_length=1)


class StockTransferRequest(InventoryRequest):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    from_location: str = Field(min_length=1)
    to_location: str = Field(min_length=1)


class InventoryResponse(InventoryOutput):
    product_id: int = Field(gt=0)
    quantity: int = Field(ge=0)
    reorder_level: int = Field(ge=0)
    is_low_stock: bool


class InventoryTransactionResponse(InventoryOutput):
    id: int
    product_id: int = Field(gt=0)
    type: InventoryTransactionType
    quantity: int
    reference: str | None
    notes: str | None
    created_at: datetime
