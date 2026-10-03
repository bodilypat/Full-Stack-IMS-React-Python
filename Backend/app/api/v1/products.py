# app/api/v1/products.py
# pyright: reportMissingImports=false

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.dependencies import get_current_user

router = APIRouter()


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    sku: str = Field(min_length=1, max_length=64)
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)
    description: Optional[str] = Field(default=None, max_length=1000)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    sku: Optional[str] = Field(default=None, min_length=1, max_length=64)
    price: Optional[float] = Field(default=None, ge=0)
    quantity: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = Field(default=None, max_length=1000)


_products = {}
_next_product_id = 1


def _get_product_or_404(product_id: int):
    product = _products.get(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


def _ensure_unique_sku(sku: str, *, exclude_id: Optional[int] = None) -> None:
    normalized_sku = sku.strip().casefold()
    if any(
        product_id != exclude_id
        and product["sku"].strip().casefold() == normalized_sku
        for product_id, product in _products.items()
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A product with this SKU already exists",
        )

@router.get("/")
def get_products(
    _current_user=Depends(get_current_user),
):
    del _current_user
    return list(_products.values())

@router.post("/")
def create_product(
    product: ProductCreate,
    _current_user=Depends(get_current_user),
):
    global _next_product_id
    del _current_user
    _ensure_unique_sku(product.sku)
    product_data = product.dict()
    product_data["sku"] = product_data["sku"].strip()
    product_data["name"] = product_data["name"].strip()
    product_data["id"] = _next_product_id
    _products[_next_product_id] = product_data
    _next_product_id += 1
    return product_data

@router.get("/{product_id}")
def get_product(
    product_id: int,
    _current_user=Depends(get_current_user),
):
    del _current_user
    return _get_product_or_404(product_id)

@router.put("/{product_id}")
def update_product(
    product_id: int,
    changes: ProductUpdate,
    _current_user=Depends(get_current_user),
):
    del _current_user
    product = _get_product_or_404(product_id)
    updates = changes.dict(exclude_unset=True)
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one product field must be provided",
        )
    if "sku" in updates:
        _ensure_unique_sku(updates["sku"], exclude_id=product_id)
        updates["sku"] = updates["sku"].strip()
    if "name" in updates:
        updates["name"] = updates["name"].strip()
    product.update(updates)
    return product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    _current_user=Depends(get_current_user),
):
    del _current_user
    _get_product_or_404(product_id)
    del _products[product_id]
    return {"message": "Product deleted", "id": product_id}
