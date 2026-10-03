# app/services/user_service.py
# pyright: reportMissingImports=false

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.core.security import hash_password
from app.schemas.user import UserCreate, UserUpdate


_USER_FIELDS = (
    "email",
    "username",
    "full_name",
    "name",
    "first_name",
    "last_name",
    "phone",
    "role",
    "is_active",
)


def _provided_values(data):
    """Return only fields explicitly supplied by the caller when possible."""
    if hasattr(data, "model_dump"):
        return data.model_dump(exclude_unset=True)
    if hasattr(data, "dict"):
        return data.dict(exclude_unset=True)
    if isinstance(data, dict):
        return data.copy()
    return {
        field: value
        for field in (*_USER_FIELDS, "password")
        if (value := getattr(data, field, None)) is not None
    }


def _user_columns(User):
    return set(User.__table__.columns.keys())


def create_user(
    db: Session,
    data: UserCreate,
):
    if db is None:
        raise ValueError("Database session is required.")
    if data is None:
        raise ValueError("User data is required.")

    values = _provided_values(data)
    password = values.pop("password", None)
    if password is None:
        raise ValueError("Password is required.")

    password_hash = hash_password(password)

    from app.models.user import User

    columns = _user_columns(User)
    user_data = {
        field: value
        for field, value in values.items()
        if field in _USER_FIELDS and field in columns
    }
    if "password_hash" in columns:
        user_data["password_hash"] = password_hash
    elif "hashed_password" in columns:
        user_data["hashed_password"] = password_hash
    elif "password" in columns:
        user_data["password"] = password_hash
    else:
        raise ValueError("User model has no supported password column.")

    try:
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise


def get_user(
    db: Session,
    user_id: int,
):
    if db is None:
        raise ValueError("Database session is required.")
    if user_id is None:
        raise ValueError("user_id is required.")

    from app.models.user import User

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise NotFoundException("User not found")
    return user


def get_users(
    db: Session,
    page: int = 1,
    limit: int = 20,
):
    if db is None:
        raise ValueError("Database session is required.")
    if page is None or page < 1:
        raise ValueError("page must be greater than zero.")
    if limit is None or limit < 1:
        raise ValueError("limit must be greater than zero.")

    from app.models.user import User

    offset = (page - 1) * limit
    return db.query(User).offset(offset).limit(limit).all()


def update_user(
    db: Session,
    user_id: int,
    data: UserUpdate,
):
    if db is None:
        raise ValueError("Database session is required.")
    if user_id is None:
        raise ValueError("user_id is required.")
    if data is None:
        raise ValueError("User update data is required.")

    from app.models.user import User

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise NotFoundException("User not found")

    values = _provided_values(data)
    columns = _user_columns(User)
    try:
        for field, value in values.items():
            if field in _USER_FIELDS and field in columns:
                setattr(user, field, value)

        password = values.get("password")
        if password is not None:
            if "password_hash" in columns:
                user.password_hash = hash_password(password)
            elif "hashed_password" in columns:
                user.hashed_password = hash_password(password)
            elif "password" in columns:
                user.password = hash_password(password)
            else:
                raise ValueError("User model has no supported password column.")
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise


def deactivate_user(
    db: Session,
    user_id: int,
):
    if db is None:
        raise ValueError("Database session is required.")
    if user_id is None:
        raise ValueError("user_id is required.")

    from app.models.user import User

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise NotFoundException("User not found")

    columns = _user_columns(User)
    try:
        if "is_active" in columns:
            user.is_active = False
        elif "active" in columns:
            user.active = False
        elif "deleted_at" in columns:
            user.deleted_at = True
        else:
            raise ValueError("User model has no supported deactivation field.")

        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise
