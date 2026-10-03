# app/api/v1/dashboard.py
# pyright: reportMissingImports=false

"""Inventory dashboard API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", summary="Get inventory dashboard metrics")
def get_dashboard(db: Session = Depends(get_db)):
	"""Return totals for products, stock, low stock, and inventory value."""
	bind = db.get_bind()
	inspector = inspect(bind)
	tables = set(inspector.get_table_names())
	table = next((name for name in ("products", "product", "items", "item") if name in tables), None)
	if table is None:
		return {
			"total_products": 0,
			"low_stock_products": 0,
			"total_units": 0,
			"inventory_value": 0.0,
		}

	columns = {column["name"] for column in inspector.get_columns(table)}
	stock = next((name for name in ("quantity", "stock_quantity", "quantity_in_stock", "stock") if name in columns), None)
	threshold = next((name for name in ("reorder_level", "minimum_stock", "min_stock") if name in columns), None)
	price = next((name for name in ("unit_price", "price", "cost_price") if name in columns), None)
	quote = bind.dialect.identifier_preparer.quote
	q_table = quote(table)

	total_products = db.execute(text(f"SELECT COUNT(*) FROM {q_table}")).scalar_one()
	total_units = 0
	low_stock_products = 0
	inventory_value = 0.0
	if stock:
		q_stock = quote(stock)
		total_units = db.execute(text(f"SELECT COALESCE(SUM({q_stock}), 0) FROM {q_table}")).scalar_one()
		if threshold:
			q_threshold = quote(threshold)
			low_stock_products = db.execute(
				text(f"SELECT COUNT(*) FROM {q_table} WHERE {q_stock} <= {q_threshold}")
			).scalar_one()
		if price:
			q_price = quote(price)
			inventory_value = db.execute(
				text(f"SELECT COALESCE(SUM({q_stock} * {q_price}), 0) FROM {q_table}")
			).scalar_one()

	return {
		"total_products": total_products,
		"low_stock_products": low_stock_products,
		"total_units": total_units,
		"inventory_value": float(inventory_value),
	}

