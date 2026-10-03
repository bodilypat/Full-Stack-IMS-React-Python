#app/api/v1/inventory.py
# pyright: reportMissingImports=false
# pyright: reportUnusedParameter=false

from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from app.api.dependencies import get_current_user

router = APIRouter()


class StockMovement(BaseModel):
    product_id: int = Field(gt=0)
    quantity: float = Field(gt=0)
    warehouse_id: Optional[int] = Field(default=None, gt=0)
    note: Optional[str] = Field(default=None, max_length=500)


class StockAdjustment(BaseModel):
    product_id: int = Field(gt=0)
    quantity: float
    warehouse_id: Optional[int] = Field(default=None, gt=0)
    reason: str = Field(min_length=1, max_length=500)


class StockTransfer(BaseModel):
    product_id: int = Field(gt=0)
    quantity: float = Field(gt=0)
    source_warehouse_id: int = Field(gt=0)
    destination_warehouse_id: int = Field(gt=0)

@router.get("/")
def get_inventory(
    current_user=Depends(get_current_user),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    search: Optional[str] = Query(default=None, min_length=1, max_length=100),
):
    _ = current_user
    return {
        "message": "Inventory list",
        "items": [],
        "page": page,
        "page_size": page_size,
        "search": search,
    }

@router.get("/low-stock")
def get_low_stock(
    current_user=Depends(get_current_user),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
):
    _ = current_user
    return {"message": "Low stock products", "items": [], "page": page, "page_size": page_size}

@router.get("/transactions")
def get_transactions(
    current_user=Depends(get_current_user),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
):
    _ = current_user
    return {"message": "Inventory transactions", "items": [], "page": page, "page_size": page_size}

@router.post("/stock-in")
def stock_in(
    movement: StockMovement,
    current_user=Depends(get_current_user),
):
    _ = current_user
    return {"message": "Stock added", "movement": movement.dict()}

@router.post("/stock-out")
def stock_out(
    movement: StockMovement,
    current_user=Depends(get_current_user),
):
    _ = current_user
    return {"message": "Stock removed", "movement": movement.dict()}

@router.post("/adjust")
def adjust_stock(
    adjustment: StockAdjustment,
    current_user=Depends(get_current_user),
):
    _ = current_user
    return {"message": "Stock adjusted", "adjustment": adjustment.dict()}

@router.post("/transfer")
def transfer_stock(
    transfer: StockTransfer,
    current_user=Depends(get_current_user),
):
    _ = current_user
    return {"message": "Stock transferred", "transfer": transfer.dict()}
