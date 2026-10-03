#app/api/v1/purchases.py

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query  # type: ignore
from pydantic import BaseModel, Field  # type: ignore
from app.api.dependencies import get_current_user  # type: ignore

router = APIRouter()


class StockRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    location_id: Optional[int] = Field(None, gt=0)
    reference: Optional[str] = None
    notes: Optional[str] = None


class AdjustmentRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ne=0)
    location_id: Optional[int] = Field(None, gt=0)
    reason: str = Field(..., min_length=1)


class TransferRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    source_location_id: int = Field(..., gt=0)
    destination_location_id: int = Field(..., gt=0)
    notes: Optional[str] = None


@router.get("/")
def get_inventory(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    _current_user=Depends(get_current_user),
):
    del _current_user
    return {"message": "Inventory list", "page": page, "page_size": page_size, "items": []}

@router.get("/low-stock")
def get_low_stock(
    threshold: int = Query(10, ge=0),
    _current_user=Depends(get_current_user),
):
    del _current_user
    return {"message": "Low stock products", "threshold": threshold, "items": []}

@router.get("/transactions")
def get_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    _current_user=Depends(get_current_user),
):
    del _current_user
    return {"message": "Inventory transactions", "page": page, "page_size": page_size, "items": []}

@router.post("/stock-in")
def stock_in(
    request: StockRequest,
    _current_user=Depends(get_current_user),
):
    del _current_user
    return {"message": "Stock added", "transaction": request.dict()}

@router.post("/stock-out")
def stock_out(
    request: StockRequest,
    _current_user=Depends(get_current_user),
):
    del _current_user
    return {"message": "Stock removed", "transaction": request.dict()}

@router.post("/adjust")
def adjust_stock(
    request: AdjustmentRequest,
    _current_user=Depends(get_current_user),
):
    del _current_user
    return {"message": "Stock adjusted", "transaction": request.dict()}

@router.post("/transfer")
def transfer_stock(
    request: TransferRequest,
    _current_user=Depends(get_current_user),
):
    del _current_user
    if request.source_location_id == request.destination_location_id:
        raise HTTPException(
            status_code=400,
            detail="Source and destination locations must differ",
        )
    return {"message": "Stock transferred", "transaction": request.dict()}
