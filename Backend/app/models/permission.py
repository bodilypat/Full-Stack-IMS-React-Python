# app/models/permission.py
# pyright: reportMissingImports=false

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.role import Role

class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = (
        UniqueConstraint("role_id", "resource", name="uq_permissions_role_resource"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
        index=True,
    )

    resource: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    can_create: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    can_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    can_update: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    can_delete: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="permissions",
    )
