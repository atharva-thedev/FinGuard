"""Pure invoice checks — no I/O. Safe to unit-test without Mongo."""

from __future__ import annotations

from datetime import datetime
from typing import Any

CONFIDENCE_THRESHOLD = 0.85


def normalize_vendor(name: str) -> str:
    return " ".join((name or "").lower().split())


def parse_date(value: str):
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(value[:10], fmt).date()
        except ValueError:
            continue
    return None


def low_confidence_fields(confidences: dict[str, float], threshold: float = CONFIDENCE_THRESHOLD) -> list[str]:
    return [k for k, v in confidences.items() if v < threshold]


def validate_invoice(data: dict[str, Any]) -> dict[str, Any]:
    fields: dict[str, list[str]] = {}
    vendor = (data.get("vendor_name") or "").strip()
    total = data.get("total")
    invoice_date = data.get("invoice_date") or ""

    if not vendor:
        fields["vendor_name"] = ["Vendor is required"]
    if total is None:
        fields["total"] = ["Amount is required"]
    if not invoice_date or parse_date(str(invoice_date)) is None:
        fields["invoice_date"] = ["A valid invoice date is required"]

    line_items = data.get("line_items") or []
    tax = data.get("tax")
    if line_items and tax is not None:
        computed = sum(float(i.get("amount") or 0) for i in line_items)
        subtotal = data.get("subtotal")
        if subtotal is not None and abs(float(subtotal) - computed) > 0.05:
            fields["subtotal"] = ["Subtotal does not match line items"]
        if total is not None and abs(float(total) - (computed + float(tax))) > 0.05:
            fields["tax"] = ["Tax plus line items does not match total"]

    return {
        "ok": not fields,
        "fields": fields,
        "normalized_date": str(parse_date(str(invoice_date)) or ""),
        "vendor_normalized": normalize_vendor(vendor),
    }


def exact_duplicate(candidate: dict[str, Any], existing: list[dict[str, Any]]) -> dict[str, Any] | None:
    inv = (candidate.get("invoice_number") or "").strip().lower()
    vendor = normalize_vendor(candidate.get("vendor_name") or "")
    if not inv or not vendor:
        return None
    cid = str(candidate.get("id") or "")
    for row in existing:
        if str(row.get("id") or "") == cid:
            continue
        if (row.get("invoice_number") or "").strip().lower() == inv and normalize_vendor(
            row.get("vendor_name") or ""
        ) == vendor:
            return row
    return None


def fuzzy_duplicate(
    candidate: dict[str, Any],
    existing: list[dict[str, Any]],
    amount_tol: float = 0.01,
    date_window_days: int = 3,
) -> dict[str, Any] | None:
    vendor = normalize_vendor(candidate.get("vendor_name") or "")
    total = candidate.get("total")
    d1 = parse_date(str(candidate.get("invoice_date") or ""))
    if not vendor or total is None or d1 is None:
        return None
    cid = str(candidate.get("id") or "")
    for row in existing:
        if str(row.get("id") or "") == cid:
            continue
        if normalize_vendor(row.get("vendor_name") or "") != vendor:
            continue
        other_total = row.get("total")
        d2 = parse_date(str(row.get("invoice_date") or ""))
        if other_total is None or d2 is None:
            continue
        if abs(float(total) - float(other_total)) / max(abs(float(total)), 1) > amount_tol:
            continue
        if abs((d1 - d2).days) <= date_window_days:
            if (candidate.get("invoice_number") or "").strip().lower() == (
                row.get("invoice_number") or ""
            ).strip().lower():
                continue
            return row
    return None


def policy_flags(
    *,
    vendor_registered: bool,
    department_spend: float,
    monthly_limit: float | None,
    require_registered_vendor: bool = True,
) -> list[str]:
    flags: list[str] = []
    if require_registered_vendor and not vendor_registered:
        flags.append("unregistered_vendor")
    if monthly_limit is not None and department_spend > monthly_limit:
        flags.append("budget_exceeded")
    return flags
