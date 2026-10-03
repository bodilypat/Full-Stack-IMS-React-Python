# app/api/v1/suppliers.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdate

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db)):
	"""Create a supplier."""
	supplier = Supplier(**payload.model_dump(exclude_unset=True))
	db.add(supplier)
	db.commit()
	db.refresh(supplier)
	return supplier


@router.get("/", response_model=List[SupplierResponse])
def list_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	"""List suppliers with pagination."""
	return db.query(Supplier).offset(skip).limit(min(limit, 500)).all()


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
	"""Get a supplier by ID."""
	supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
	if supplier is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
	return supplier


@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
	supplier_id: int, payload: SupplierUpdate, db: Session = Depends(get_db)
):
	"""Update a supplier."""
	supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
	if supplier is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")

	for field, value in payload.model_dump(exclude_unset=True).items():
		setattr(supplier, field, value)
	db.commit()
	db.refresh(supplier)
	return supplier


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
	"""Delete a supplier."""
	supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
	if supplier is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
	db.delete(supplier)
	db.commit()

