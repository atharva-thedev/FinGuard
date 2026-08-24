from datetime import datetime

from pydantic import BaseModel


class LineItemSchema(BaseModel):
    description: str = ""
    quantity: float = 1.0
    unit_price: float = 0.0
    amount: float = 0.0


class UpdateExtractionRequest(BaseModel):
    vendor_name: str | None = None
    invoice_number: str | None = None
    invoice_date: str | None = None
    due_date: str | None = None
    line_items: list[LineItemSchema] | None = None
    subtotal: float | None = None
    tax: float | None = None
    total: float | None = None
    category: str | None = None
    department: str | None = None
    override_reason: str | None = None


class InvoiceResponse(BaseModel):
    id: str
    organization_id: str
    uploaded_by: str
    status: str
    original_filename: str
    content_type: str
    vendor_name: str
    invoice_number: str
    invoice_date: str
    due_date: str
    line_items: list[LineItemSchema]
    subtotal: float | None
    tax: float | None
    total: float | None
    field_confidences: dict[str, float]
    category: str
    department: str
    duplicate_of: str | None
    duplicate_warning: str | None
    policy_flags: list[str]
    override_reason: str | None
    created_at: datetime
    updated_at: datetime
