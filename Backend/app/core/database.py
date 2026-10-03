#app/core/database.py

# pyright: reportMissingImports=false

from collections.abc import Generator

from sqlalchemy import create_engine  # type: ignore[import-not-found]
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker  # type: ignore[import-not-found]

from app.core.config import settings  # type: ignore[import-not-found]

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
