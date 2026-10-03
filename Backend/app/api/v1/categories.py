#app/api/v1/categories.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
	return db.query(Category).all()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
	category = db.query(Category).filter(Category.id == category_id).first()
	if category is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
	return category


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
	category = Category(**category_data.model_dump())
	db.add(category)
	db.commit()
	db.refresh(category)
	return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
	category_id: int,
	category_data: CategoryUpdate,
	db: Session = Depends(get_db),
):
	category = db.query(Category).filter(Category.id == category_id).first()
	if category is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

	for field, value in category_data.model_dump(exclude_unset=True).items():
		setattr(category, field, value)
	db.commit()
	db.refresh(category)
	return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
	category = db.query(Category).filter(Category.id == category_id).first()
	if category is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
	db.delete(category)
	db.commit()

