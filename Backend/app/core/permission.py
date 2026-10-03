# app/core/permissions.py

from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"


class Permission(str, Enum):
    VIEW_PRODUCTS = "view_products"
    MANAGE_PRODUCTS = "manage_products"

    VIEW_INVENTORY = "view_inventory"
    MANAGE_INVENTORY = "manage_inventory"

    VIEW_PURCHASES = "view_purchases"
    MANAGE_PURCHASES = "manage_purchases"

    VIEW_SALES = "view_sales"
    MANAGE_SALES = "manage_sales"

    VIEW_REPORTS = "view_reports"

    MANAGE_USERS = "manage_users"


ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    Role.ADMIN: frozenset(Permission),
    Role.MANAGER: frozenset(Permission) - {Permission.MANAGE_USERS},
    Role.STAFF: frozenset(
        {
            Permission.VIEW_PRODUCTS,
            Permission.VIEW_INVENTORY,
            Permission.VIEW_SALES,
            Permission.MANAGE_SALES,
        }
    ),
}


def permissions_for_role(role: Role) -> frozenset[Permission]:
    """Return all permissions granted to a role."""
    return ROLE_PERMISSIONS[Role(role)]


def has_permission(role: Role, permission: Permission) -> bool:
    """Return whether a role is granted the requested permission."""
    return Permission(permission) in permissions_for_role(role)
