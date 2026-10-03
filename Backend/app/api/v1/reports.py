# app/api/v1/reports.py

from datetime import date, datetime, time, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import MetaData, Table, func, inspect, select
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(prefix="/reports", tags=["Reports"])

def _reflect_table(db: Session, candidates: tuple[str, ...]) -> Table:
	"""Reflect the first matching table so reports work with common schema names."""
	inspector = inspect(db.get_bind())
	table_names = set(inspector.get_table_names())
	name = next((candidate for candidate in candidates if candidate in table_names), None)
	if name is None:
		raise HTTPException(status_code=503, detail=f"Required table not found: {', '.join(candidates)}")
	return Table(name, MetaData(), autoload_with=db.get_bind())


def _column(table: Table, *names: str):
	return next((table.c[name] for name in names if name in table.c), None)

@router.get("/inventory", summary="Inventory overview")
def inventory_report(db: Session = Depends(get_db)):
	"""Summarize product count, units in stock, and stock value."""
	products = _reflect_table(db, ("products", "product"))
	quantity = _column(products, "quantity", "stock", "stock_quantity", "quantity_in_stock")
	price = _column(products, "unit_price", "price", "cost_price", "purchase_price")
	if quantity is None:
		raise HTTPException(status_code=503, detail="Product table has no recognized stock quantity column")

	value = func.coalesce(func.sum(quantity * price), 0) if price is not None else 0
	statement = select(
		func.count().label("product_count"),
		func.coalesce(func.sum(quantity), 0).label("units_in_stock"),
		value.label("inventory_value"),
	).select_from(products)
	return dict(db.execute(statement).mappings().one())

@router.get("/low-stock", summary="Products at or below their reorder level")
def low_stock_report(db: Session = Depends(get_db)):
	products = _reflect_table(db, ("products", "product"))
	quantity = _column(products, "quantity", "stock", "stock_quantity", "quantity_in_stock")
	reorder_level = _column(products, "reorder_level", "min_stock", "minimum_stock", "alert_quantity")
	if quantity is None or reorder_level is None:
		raise HTTPException(status_code=503, detail="Product table lacks stock or reorder-level columns")

	statement = select(products).where(quantity <= reorder_level).order_by(quantity.asc())
	return [dict(row) for row in db.execute(statement).mappings().all()]

@router.get("/sales", summary="Sales totals for a date range")
def sales_report(
	start_date: date = Query(default_factory=lambda: date.today() - timedelta(days=30)),
	end_date: date = Query(default_factory=date.today),
	db: Session = Depends(get_db),
):
	if start_date > end_date:
		raise HTTPException(status_code=422, detail="start_date must be on or before end_date")

	sales = _reflect_table(db, ("sales", "orders", "invoices"))
	date_column = _column(sales, "sale_date", "created_at", "date", "order_date", "invoice_date")
	amount = _column(sales, "total_amount", "total", "amount", "grand_total")
	if date_column is None or amount is None:
		raise HTTPException(status_code=503, detail="Sales table lacks a recognized date or total column")

	statement = select(
		func.count().label("transaction_count"),
		func.coalesce(func.sum(amount), 0).label("total_sales"),
	).select_from(sales).where(
		date_column >= datetime.combine(start_date, time.min),
		date_column < datetime.combine(end_date + timedelta(days=1), time.min),
	)
	totals = db.execute(statement).mappings().one()
	return {
		"start_date": start_date,
		"end_date": end_date,
		"transaction_count": totals["transaction_count"],
		"total_sales": totals["total_sales"],
	}

