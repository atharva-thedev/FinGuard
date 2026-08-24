from __future__ import annotations

from typing import Any, Protocol

import httpx

from app.config.env import settings
from app.domain.invoice_rules import CONFIDENCE_THRESHOLD


class ExtractionResult(dict):
    """vendor_name, invoice_number, invoice_date, due_date, line_items, subtotal, tax, total, confidences"""


class ExtractionProvider(Protocol):
    async def extract(self, *, filename: str, content: bytes, content_type: str) -> dict[str, Any]: ...


class MockExtractionProvider:
    async def extract(self, *, filename: str, content: bytes, content_type: str) -> dict[str, Any]:
        low = "lowconf" in filename.lower()
        conf = 0.5 if low else 0.96
        return {
            "vendor_name": "Acme Supplies",
            "invoice_number": "INV-1001",
            "invoice_date": "2026-08-01",
            "due_date": "2026-08-31",
            "line_items": [
                {"description": "Office paper", "quantity": 10, "unit_price": 5.0, "amount": 50.0}
            ],
            "subtotal": 50.0,
            "tax": 5.0,
            "total": 55.0,
            "confidences": {
                "vendor_name": conf,
                "invoice_number": conf,
                "invoice_date": conf,
                "total": conf,
            },
            "confidence_threshold": CONFIDENCE_THRESHOLD,
        }


class HttpExtractionProvider:
    async def extract(self, *, filename: str, content: bytes, content_type: str) -> dict[str, Any]:
        if not settings.extraction_http_url:
            raise RuntimeError("EXTRACTION_HTTP_URL is not set")
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                settings.extraction_http_url,
                files={"file": (filename, content, content_type)},
            )
            response.raise_for_status()
            return response.json()


def get_provider() -> ExtractionProvider:
    if settings.extraction_provider == "http":
        return HttpExtractionProvider()
    return MockExtractionProvider()
