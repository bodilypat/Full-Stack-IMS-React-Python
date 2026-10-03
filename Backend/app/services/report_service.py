# app/services/report_service.py

from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session  # type: ignore

from app.schemas.report import ReportDateRange  # type: ignore

def _resolve_date_range(date_range: ReportDateRange | None) -> tuple[date | None, date | None]:
    if date_range is None:
        return None, None

    start_date = getattr(date_range, "start_date", None)
    if start_date is None:
        start_date = getattr(date_range, "start", None)

    end_date = getattr(date_range, "end_date", None)
    if end_date is None:
        end_date = getattr(date_range, "end", None)

    return start_date, end_date

def _validate_session(db: Session) -> Session:
    if db is None:
        raise ValueError("Database session is required.")
    return db

def get_sales_report(
    db: Session,
    date_range: ReportDateRange,
):
    session = _validate_session(db)
    start_date, end_date = _resolve_date_range(date_range)

    _ = session
    return {
        "report_type": "sales",
        "start_date": start_date,
        "end_date": end_date,
        "items": [],
    }

def get_purchase_report(
    db: Session,
    date_range: ReportDateRange,
):
    session = _validate_session(db)
    start_date, end_date = _resolve_date_range(date_range)

    _ = session
    return {
        "report_type": "purchase",
        "start_date": start_date,
        "end_date": end_date,
        "items": [],
    }

def get_inventory_report(
    db: Session,
):
    session = _validate_session(db)

    _ = session
    return {
        "report_type": "inventory",
        "items": [],
    }

def get_stock_movement_report(
    db: Session,
    date_range: ReportDateRange,
):
    session = _validate_session(db)
    start_date, end_date = _resolve_date_range(date_range)

    _ = session
    return {
        "report_type": "stock_movement",
        "start_date": start_date,
        "end_date": end_date,
        "items": [],
    }

def get_product_performance_report(
    db: Session,
    date_range: ReportDateRange,
):
    session = _validate_session(db)
    start_date, end_date = _resolve_date_range(date_range)

    _ = session
    return {
        "report_type": "product_performance",
        "start_date": start_date,
        "end_date": end_date,
        "items": [],
    }

