#app/api/v1/router.py

from fastapi import APIRouter  # type: ignore[import-not-found]

from app.api.v1 import (  # type: ignore[import-not-found]
    auth,
    users,
    products,
    categories,
    suppliers,
    customers,
    inventory,
    purchases,
    sales,
    payments,
    dashboard,
    reports,
)

api_router = APIRouter()

# Keep each API prefix and its documentation tag together for consistency.
_route_config = (
    (auth.router, "/auth", "Authentication"),
    (users.router, "/users", "Users"),
    (products.router, "/products", "Products"),
    (categories.router, "/categories", "Categories"),
    (suppliers.router, "/suppliers", "Suppliers"),
    (customers.router, "/customers", "Customers"),
    (inventory.router, "/inventory", "Inventory"),
    (purchases.router, "/purchases", "Purchases"),
    (sales.router, "/sales", "Sales"),
    (payments.router, "/payments", "Payments"),
    (dashboard.router, "/dashboard", "Dashboard"),
    (reports.router, "/reports", "Reports"),
)

for router, prefix, tag in _route_config:
    api_router.include_router(router, prefix=prefix, tags=[tag])
