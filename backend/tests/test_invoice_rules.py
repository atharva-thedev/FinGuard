from app.domain.invoice_rules import (
    exact_duplicate,
    fuzzy_duplicate,
    low_confidence_fields,
    normalize_vendor,
    parse_date,
    policy_flags,
    validate_invoice,
)


def test_normalize_vendor():
    assert normalize_vendor("  Acme  Corp,   LLC ") == "acme corp, llc"
    assert normalize_vendor("") == ""


def test_parse_date():
    assert str(parse_date("2026-08-01")) == "2026-08-01"
    assert str(parse_date("08/01/2026")) == "2026-08-01"
    assert str(parse_date("01/08/2026")) == "2026-01-08"
    assert parse_date("invalid-date") is None


def test_validate_invoice_valid():
    data = {
        "vendor_name": "Acme Supplies",
        "total": 100.0,
        "invoice_date": "2026-08-01",
        "subtotal": 90.0,
        "tax": 10.0,
        "line_items": [{"description": "Item 1", "quantity": 1, "unit_price": 90.0, "amount": 90.0}],
    }
    res = validate_invoice(data)
    assert res["ok"] is True
    assert res["fields"] == {}


def test_validate_invoice_missing_fields():
    data = {
        "vendor_name": "",
        "total": None,
        "invoice_date": "not-a-date",
    }
    res = validate_invoice(data)
    assert res["ok"] is False
    assert "vendor_name" in res["fields"]
    assert "total" in res["fields"]
    assert "invoice_date" in res["fields"]


def test_validate_invoice_tax_mismatch():
    data = {
        "vendor_name": "Acme Supplies",
        "total": 120.0,  # Line items 90 + Tax 10 = 100 != 120
        "invoice_date": "2026-08-01",
        "subtotal": 90.0,
        "tax": 10.0,
        "line_items": [{"description": "Item 1", "quantity": 1, "unit_price": 90.0, "amount": 90.0}],
    }
    res = validate_invoice(data)
    assert res["ok"] is False
    assert "tax" in res["fields"]


def test_exact_duplicate():
    cand = {"id": "1", "invoice_number": "INV-1001", "vendor_name": "Acme Corp"}
    existing = [
        {"id": "2", "invoice_number": "inv-1001", "vendor_name": "ACME CORP"},
        {"id": "3", "invoice_number": "INV-1002", "vendor_name": "Acme Corp"},
    ]
    dup = exact_duplicate(cand, existing)
    assert dup is not None
    assert dup["id"] == "2"


def test_fuzzy_duplicate():
    cand = {
        "id": "1",
        "invoice_number": "INV-1001-A",
        "vendor_name": "Acme Corp",
        "total": 100.0,
        "invoice_date": "2026-08-05",
    }
    existing = [
        {
            "id": "2",
            "invoice_number": "INV-1001-B",
            "vendor_name": "Acme Corp",
            "total": 100.0,
            "invoice_date": "2026-08-06",
        }
    ]
    dup = fuzzy_duplicate(cand, existing)
    assert dup is not None
    assert dup["id"] == "2"


def test_policy_flags():
    flags = policy_flags(
        vendor_registered=False,
        department_spend=1500.0,
        monthly_limit=1000.0,
        require_registered_vendor=True,
    )
    assert "unregistered_vendor" in flags
    assert "budget_exceeded" in flags


def test_low_confidence_fields():
    confidences = {
        "vendor_name": 0.95,
        "invoice_number": 0.80,
        "total": 0.50,
    }
    low = low_confidence_fields(confidences, threshold=0.85)
    assert "invoice_number" in low
    assert "total" in low
    assert "vendor_name" not in low
