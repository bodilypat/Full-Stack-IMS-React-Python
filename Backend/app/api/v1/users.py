# app/api/v1/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
	username: str = Field(min_length=1, max_length=100)
	email: EmailStr
	full_name: str | None = Field(default=None, max_length=200)
	role: str = Field(default="staff", min_length=1, max_length=50)


class UserUpdate(BaseModel):
	username: str | None = Field(default=None, min_length=1, max_length=100)
	email: EmailStr | None = None
	full_name: str | None = Field(default=None, max_length=200)
	role: str | None = Field(default=None, min_length=1, max_length=50)
	is_active: bool | None = None


class UserResponse(BaseModel):
	id: int
	username: str
	email: EmailStr
	full_name: str | None = None
	role: str
	is_active: bool

	model_config = ConfigDict(from_attributes=True)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
	existing = db.query(User).filter(
		(User.username == user_data.username) | (User.email == user_data.email)
	).first()
	if existing:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")

	user = User(**user_data.model_dump(), is_active=True)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user


@router.get("/", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	return db.query(User).offset(max(skip, 0)).limit(min(max(limit, 1), 100)).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
	user = db.query(User).filter(User.id == user_id).first()
	if user is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
	return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
	user = db.query(User).filter(User.id == user_id).first()
	if user is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

	changes = user_data.model_dump(exclude_unset=True)
	for field in ("username", "email"):
		value = changes.get(field)
		if value is not None:
			duplicate = db.query(User).filter(
				getattr(User, field) == value, User.id != user_id
			).first()
			if duplicate:
				raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{field} already exists")
	for field, value in changes.items():
		setattr(user, field, value)
	db.commit()
	db.refresh(user)
	return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
	user = db.query(User).filter(User.id == user_id).first()
	if user is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
	db.delete(user)
	db.commit()

