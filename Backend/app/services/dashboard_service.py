# app/services/dashboard_service.py

from typing import Any

Session = Any

def _first(row: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if row.get(key) is not None:
            return row[key]
    return default


def _number(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0

def _rows(db: Session, candidates: tuple[str, ...]) -> list[dict[str, Any]]:
    """Read rows from the first available table in common schema variants."""
    try:
        from sqlalchemy import MetaData, Table, inspect, select  # type: ignore[import-not-found]
    except ImportError:
        return []

    bind = db.get_bind()
    available = set(inspect(bind).get_table_names())
    name = next((candidate for candidate in candidates if candidate in available), None)
    if name is None:
        return []
    table = Table(name, MetaData(), autoload_with=bind)
    return [dict(row) for row in db.execute(select(table)).mappings().all()]

def get_dashboard(
    db: Session | None = None,
):
    result = {
        "stats": {
            "total_products": 0,
            "total_inventory_units": 0,
            "inventory_value": 0,
            "total_sales": 0,
            "total_purchases": 0,
            "low_stock_count": 0,
        },
        "sales": [],
        "top_products": [],
    }
    if db is None:
        return result

    products = _rows(db, ("products", "product"))
    sales = _rows(db, ("sales", "sale", "orders"))
    purchases = _rows(db, ("purchases", "purchase"))
    sale_items = _rows(
        db, ("sale_items", "sales_items", "sale_details", "sales_details", "order_items")
    )

    product_quantities: dict[Any, float] = {}
    product_names: dict[Any, str] = {}
    for product in products:
        product_id = _first(product, "id", "product_id")
        quantity = _number(
            _first(product, "quantity", "stock", "stock_quantity", "units_in_stock")
        )
        product_quantities[product_id] = quantity
        if product_id is not None:
            product_names[product_id] = str(
                _first(product, "name", "product_name", default=product_id)
            )

    result["stats"]["total_products"] = len(products)
    result["stats"]["total_inventory_units"] = sum(product_quantities.values())
    result["stats"]["inventory_value"] = sum(
        product_quantities.get(_first(product, "id", "product_id"), 0)
        * _number(_first(product, "cost_price", "unit_cost", "purchase_price", "price"))
        for product in products
    )
    result["stats"]["low_stock_count"] = sum(
        product_quantities.get(_first(product, "id", "product_id"), 0)
        <= _number(_first(product, "reorder_level", "low_stock_threshold", "min_stock", default=5))
        for product in products
    )

    def total(row: dict[str, Any]) -> float:
        return _number(_first(row, "total_amount", "grand_total", "total", "amount"))

    result["stats"]["total_sales"] = sum(total(row) for row in sales)
    result["stats"]["total_purchases"] = sum(total(row) for row in purchases)

    sales_by_day: dict[str, float] = {}
    for sale in sales:
        date = _first(sale, "sale_date", "created_at", "date", "transaction_date")
        if date is not None:
            day = date.isoformat()[:10] if hasattr(date, "isoformat") else str(date)[:10]
            sales_by_day[day] = sales_by_day.get(day, 0) + total(sale)
    result["sales"] = [
        {"date": day, "total": amount} for day, amount in sorted(sales_by_day.items())
    ]

    quantities_sold: dict[Any, float] = {}
    for item in sale_items:
        product_id = _first(item, "product_id", "product")
        if product_id is not None:
            quantities_sold[product_id] = quantities_sold.get(product_id, 0) + _number(
                _first(item, "quantity", "qty", "units")
            )
    result["top_products"] = [
        {
            "product_id": product_id,
            "name": product_names.get(product_id, str(product_id)),
            "quantity_sold": quantity,
        }
        for product_id, quantity in sorted(
            quantities_sold.items(), key=lambda item: item[1], reverse=True
        )[:5]
    ]
    return result
