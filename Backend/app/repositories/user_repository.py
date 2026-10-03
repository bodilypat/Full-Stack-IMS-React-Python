#app/repositories/user_repository.py

from sqlalchemy import select  # type: ignore[import-not-found]
from sqlalchemy.orm import Session  # type: ignore[import-not-found]

from app.models.user import User  # type: ignore[import-not-found]

def get_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    return db.get(User, user_id)

def get_by_email(
    db: Session,
    email: str,
) -> User | None:
    statement = select(User).where(
        User.email == email
    )

    return db.scalar(statement)

def get_all(
    db: Session,
    offset: int = 0,
    limit: int = 20,
) -> list[User]:
    if offset < 0:
        raise ValueError("offset must be non-negative")
    if limit <= 0:
        raise ValueError("limit must be positive")

    statement = (
        select(User)
        .order_by(User.id.desc())
        .offset(offset)
        .limit(limit)
    )

    return list(db.scalars(statement).all())

def create(
    db: Session,
    user: User,
) -> User:
    db.add(user)
    db.flush()
    db.refresh(user)

    return user

def update(
    db: Session,
    user: User,
) -> User:
    db.add(user)
    db.flush()
    db.refresh(user)

    return user

def delete(
    db: Session,
    user: User,
) -> None:
    db.delete(user)
    db.flush()

