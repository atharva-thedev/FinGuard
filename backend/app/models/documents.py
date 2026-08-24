from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field
from pymongo import ASCENDING, IndexModel


from app.utils.datetime import utcnow


class UserRole(StrEnum):
    admin = "admin"
    controller = "controller"
    approver = "approver"
    ap_clerk = "ap_clerk"
    viewer = "viewer"


class InvoiceStatus(StrEnum):
    captured = "captured"
    extracting = "extracting"
    needs_review = "needs_review"
    validated = "validated"
    pending_approval = "pending_approval"
    exception = "exception"
    approved = "approved"
    rejected = "rejected"


class ExceptionType(StrEnum):
    duplicate = "duplicate"
    policy = "policy"
    budget = "budget"
    tax = "tax"
    missing_fields = "missing_fields"


class ApprovalMode(StrEnum):
    sequential = "sequential"
    parallel = "parallel"


class LineItem(BaseModel):
    description: str = ""
    quantity: float = 1
    unit_price: float = 0
    amount: float = 0


class Organization(Document):
    name: str
    slug: Indexed(str, unique=True)
    approval_threshold: float = 0
    is_deleted: bool = False
    created_at: datetime = Field(default_factory=utcnow)

    class Settings:
        name = "organizations"


class User(Document):
    organization_id: str
    email: Indexed(EmailStr, unique=True)
    password_hash: str | None = None
    google_sub: str | None = None
    full_name: str
    role: UserRole
    department: str = ""
    failed_login_count: int = 0
    locked_until: datetime | None = None
    is_deleted: bool = False
    created_at: datetime = Field(default_factory=utcnow)

    class Settings:
        name = "users"
        indexes = [IndexModel([("organization_id", ASCENDING)])]


class Session(Document):
    user_id: str
    organization_id: str
    refresh_hash: str
    user_agent: str = ""
    revoked: bool = False
    created_at: datetime = Field(default_factory=utcnow)
    expires_at: datetime

    class Settings:
        name = "sessions"


class Vendor(Document):
    organization_id: str
    name: str
    normalized_name: str
    registered: bool = True
    is_deleted: bool = False
    created_at: datetime = Field(default_factory=utcnow)

    class Settings:
        name = "vendors"
        indexes = [
            IndexModel(
                [("organization_id", ASCENDING), ("normalized_name", ASCENDING)],
                unique=True,
            )
        ]


class Category(Document):
    organization_id: str
    name: str
    is_deleted: bool = False

    class Settings:
        name = "categories"


class CategoryOverride(Document):
    organization_id: str
    vendor_normalized: str
    category: str

    class Settings:
        name = "category_overrides"


class BudgetRule(Document):
    organization_id: str
    department: str
    category: str
    monthly_limit: float
    is_deleted: bool = False

    class Settings:
        name = "budget_rules"


class PolicyRule(Document):
    organization_id: str
    code: str
    enabled: bool = True
    config: dict[str, Any] = Field(default_factory=dict)
    is_deleted: bool = False

    class Settings:
        name = "policy_rules"


class Invoice(Document):
    organization_id: str
    uploaded_by: str
    status: InvoiceStatus = InvoiceStatus.captured
    original_filename: str
    stored_path: str
    content_type: str
    vendor_name: str = ""
    vendor_normalized: str = ""
    invoice_number: str = ""
    invoice_date: str = ""
    due_date: str = ""
    line_items: list[LineItem] = Field(default_factory=list)
    subtotal: float | None = None
    tax: float | None = None
    total: float | None = None
    field_confidences: dict[str, float] = Field(default_factory=dict)
    category: str = "Other"
    department: str = ""
    duplicate_of: str | None = None
    duplicate_warning: str | None = None
    policy_flags: list[str] = Field(default_factory=list)
    override_reason: str | None = None
    is_deleted: bool = False
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)

    class Settings:
        name = "invoices"
        indexes = [
            IndexModel([("organization_id", ASCENDING), ("invoice_number", ASCENDING)])
        ]


class InvoiceException(Document):
    organization_id: str
    invoice_id: str
    type: ExceptionType
    status: str = "open"
    notes: str = ""
    is_deleted: bool = False
    created_at: datetime = Field(default_factory=utcnow)

    class Settings:
        name = "exceptions"


class Approval(Document):
    organization_id: str
    invoice_id: str
    mode: ApprovalMode = ApprovalMode.sequential
    steps: list[str] = Field(default_factory=list)
    current_step: int = 0
    status: str = "pending"
    decided_by: str | None = None
    comment: str = ""
    is_deleted: bool = False
    created_at: datetime = Field(default_factory=utcnow)

    class Settings:
        name = "approvals"


class AuditLog(Document):
    organization_id: str
    actor_id: str
    action: str
    resource_type: str
    resource_id: str
    before: dict[str, Any] | None = None
    after: dict[str, Any] | None = None
    created_at: datetime = Field(default_factory=utcnow)

    class Settings:
        name = "audit_logs"


DOCUMENT_MODELS = [
    Organization,
    User,
    Session,
    Vendor,
    Category,
    CategoryOverride,
    BudgetRule,
    PolicyRule,
    Invoice,
    InvoiceException,
    Approval,
    AuditLog,
]
