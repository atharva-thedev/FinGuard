from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Any

from fastapi import UploadFile

from app.utils.datetime import utcnow

from app.config.env import settings
from app.core.errors import AppError
from app.domain.invoice_rules import (
    exact_duplicate,
    fuzzy_duplicate,
    low_confidence_fields,
    normalize_vendor,
    policy_flags,
    validate_invoice,
)
from app.domain.taxonomy import DEFAULT_CATEGORIES, guess_category
from app.models.documents import (
    Approval,
    BudgetRule,
    Category,
    CategoryOverride,
    Invoice,
    InvoiceException,
    InvoiceStatus,
    LineItem,
    Organization,
    PolicyRule,
    User,
    UserRole,
    Vendor,
)
from app.modules.extraction.provider import get_provider
from app.realtime.hub import hub
from app.utils.audit import write_audit
from app.utils.ownership import assert_org_access

ALLOWED_TYPES = {"application/pdf", "image/jpeg", "image/png"}
ALLOWED_EXT = {".pdf", ".jpg", ".jpeg", ".png"}


def _invoice_as_dict(inv: Invoice) -> dict:
    return {
        "id": str(inv.id),
        "vendor_name": inv.vendor_name,
        "invoice_number": inv.invoice_number,
        "invoice_date": inv.invoice_date,
        "total": inv.total,
    }


def format_invoice(inv: Invoice) -> dict:
    return {
        "id": str(inv.id),
        "organization_id": str(inv.organization_id),
        "uploaded_by": str(inv.uploaded_by),
        "status": inv.status.value,
        "original_filename": inv.original_filename,
        "content_type": inv.content_type,
        "vendor_name": inv.vendor_name,
        "invoice_number": inv.invoice_number,
        "invoice_date": inv.invoice_date,
        "due_date": inv.due_date,
        "line_items": [i.model_dump() for i in inv.line_items],
        "subtotal": inv.subtotal,
        "tax": inv.tax,
        "total": inv.total,
        "field_confidences": inv.field_confidences,
        "category": inv.category,
        "department": inv.department,
        "duplicate_of": inv.duplicate_of,
        "duplicate_warning": inv.duplicate_warning,
        "policy_flags": inv.policy_flags,
        "override_reason": inv.override_reason,
        "created_at": inv.created_at,
        "updated_at": inv.updated_at,
    }


async def seed_org_defaults(org_id: str) -> None:
    existing = await Category.find(Category.organization_id == org_id).count()
    if existing:
        return
    for name in DEFAULT_CATEGORIES:
        await Category(organization_id=org_id, name=name).insert()
    await PolicyRule(
        organization_id=org_id,
        code="registered_vendor",
        enabled=True,
        config={},
    ).insert()


async def save_upload(org_id: str, upload: UploadFile) -> tuple[str, str, str]:
    filename = upload.filename or "invoice.bin"
    ext = Path(filename).suffix.lower()
    content_type = upload.content_type or "application/octet-stream"
    if content_type not in ALLOWED_TYPES or ext not in ALLOWED_EXT:
        raise AppError("VALIDATION_ERROR", "Only PDF, JPG, and PNG invoices are accepted", 400)

    dest_dir = Path(settings.upload_dir) / org_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    stored = dest_dir / f"{uuid.uuid4().hex}{ext}"
    data = await upload.read()
    if len(data) > settings.max_upload_bytes:
        raise AppError("VALIDATION_ERROR", "File exceeds 25 MB limit", 400)
    stored.write_bytes(data)
    return filename, str(stored), content_type


async def create_from_uploads(
    *,
    user: User,
    files: list[UploadFile],
    department: str = "",
) -> list[Invoice]:
    if len(files) > 50:
        raise AppError("VALIDATION_ERROR", "Batch upload is limited to 50 files", 400)
    created: list[Invoice] = []
    for upload in files:
        original, path, ctype = await save_upload(str(user.organization_id), upload)
        invoice = Invoice(
            organization_id=str(user.organization_id),
            uploaded_by=str(user.id),
            original_filename=original,
            stored_path=path,
            content_type=ctype,
            department=department,
            status=InvoiceStatus.captured,
        )
        await invoice.insert()
        created.append(invoice)
        await write_audit(
            organization_id=str(user.organization_id),
            actor_id=str(user.id),
            action="invoice.captured",
            resource_type="invoice",
            resource_id=str(invoice.id),
            after={"filename": original},
        )
        await hub.broadcast(
            str(user.organization_id),
            {"event": "invoice.created", "invoice_id": str(invoice.id)},
        )
        await run_pipeline(str(invoice.id), actor_id=str(user.id))
    return created


async def run_pipeline(invoice_id: str, actor_id: str) -> Invoice:
    invoice = await Invoice.get(invoice_id)
    if invoice is None or invoice.is_deleted:
        raise AppError("NOT_FOUND", "Invoice not found", 404)

    invoice.status = InvoiceStatus.extracting
    invoice.updated_at = utcnow()
    await invoice.save()

    raw = Path(invoice.stored_path).read_bytes() if os.path.exists(invoice.stored_path) else b""
    extracted = await get_provider().extract(
        filename=invoice.original_filename,
        content=raw,
        content_type=invoice.content_type,
    )

    invoice.vendor_name = extracted.get("vendor_name") or ""
    invoice.vendor_normalized = normalize_vendor(invoice.vendor_name)
    invoice.invoice_number = extracted.get("invoice_number") or ""
    invoice.invoice_date = extracted.get("invoice_date") or ""
    invoice.due_date = extracted.get("due_date") or ""
    invoice.subtotal = extracted.get("subtotal")
    invoice.tax = extracted.get("tax")
    invoice.total = extracted.get("total")
    invoice.field_confidences = extracted.get("confidences") or {}
    items = extracted.get("line_items") or []
    invoice.line_items = [LineItem(**i) if isinstance(i, dict) else i for i in items]

    override = await CategoryOverride.find_one(
        CategoryOverride.organization_id == invoice.organization_id,
        CategoryOverride.vendor_normalized == invoice.vendor_normalized,
    )
    invoice.category = override.category if override else guess_category(invoice.vendor_name)

    validation = validate_invoice(
        {
            "vendor_name": invoice.vendor_name,
            "total": invoice.total,
            "invoice_date": invoice.invoice_date,
            "subtotal": invoice.subtotal,
            "tax": invoice.tax,
            "line_items": [i.model_dump() for i in invoice.line_items],
        }
    )

    others = await Invoice.find(
        Invoice.organization_id == invoice.organization_id,
        Invoice.is_deleted == False,
        Invoice.id != invoice.id,
    ).to_list()
    existing = [_invoice_as_dict(i) for i in others]
    cand = _invoice_as_dict(invoice)
    exact = exact_duplicate(cand, existing)
    fuzzy = None if exact else fuzzy_duplicate(cand, existing)

    if exact:
        invoice.duplicate_of = str(exact["id"])
        invoice.status = InvoiceStatus.exception
        await invoice.save()
        await InvoiceException(
            organization_id=invoice.organization_id,
            invoice_id=str(invoice.id),
            type="duplicate",
            notes="Exact duplicate of an existing invoice",
        ).insert()
        await _notify(invoice)
        return invoice

    if fuzzy:
        invoice.duplicate_warning = f"Possible duplicate of {fuzzy['id']}"

    vendor = await Vendor.find_one(
        Vendor.organization_id == invoice.organization_id,
        Vendor.normalized_name == invoice.vendor_normalized,
        Vendor.is_deleted == False,
    )
    policy = await PolicyRule.find_one(
        PolicyRule.organization_id == invoice.organization_id,
        PolicyRule.code == "registered_vendor",
        PolicyRule.is_deleted == False,
    )
    spend = 0.0
    if invoice.department and invoice.total is not None:
        month = utcnow().strftime("%Y-%m")
        dept_invoices = await Invoice.find(
            Invoice.organization_id == invoice.organization_id,
            Invoice.department == invoice.department,
            Invoice.is_deleted == False,
        ).to_list()
        spend = sum(
            (i.total or 0)
            for i in dept_invoices
            if i.created_at.strftime("%Y-%m") == month and i.status == InvoiceStatus.approved
        ) + float(invoice.total)
    budget = None
    if invoice.department:
        budget = await BudgetRule.find_one(
            BudgetRule.organization_id == invoice.organization_id,
            BudgetRule.department == invoice.department,
            BudgetRule.category == invoice.category,
            BudgetRule.is_deleted == False,
        )
    flags = policy_flags(
        vendor_registered=bool(vendor and vendor.registered),
        department_spend=spend,
        monthly_limit=budget.monthly_limit if budget else None,
        require_registered_vendor=bool(policy and policy.enabled),
    )
    invoice.policy_flags = flags

    low = low_confidence_fields(invoice.field_confidences)
    if not validation["ok"] or low:
        invoice.status = InvoiceStatus.needs_review
        if not validation["ok"]:
            await InvoiceException(
                organization_id=invoice.organization_id,
                invoice_id=str(invoice.id),
                type="missing_fields",
                notes=str(validation["fields"]),
            ).insert()
    elif flags:
        invoice.status = InvoiceStatus.exception
        etype = "budget" if "budget_exceeded" in flags else "policy"
        await InvoiceException(
            organization_id=invoice.organization_id,
            invoice_id=str(invoice.id),
            type=etype,
            notes=",".join(flags),
        ).insert()
    else:
        invoice.status = InvoiceStatus.validated
        await _open_approval(invoice)

    invoice.updated_at = utcnow()
    await invoice.save()
    await write_audit(
        organization_id=invoice.organization_id,
        actor_id=actor_id,
        action="invoice.processed",
        resource_type="invoice",
        resource_id=str(invoice.id),
        after={"status": invoice.status.value},
    )
    await _notify(invoice)
    return invoice


async def _open_approval(invoice: Invoice) -> None:
    org = await Organization.get(invoice.organization_id)
    threshold = org.approval_threshold if org else 0
    if invoice.total is not None and invoice.total < threshold:
        invoice.status = InvoiceStatus.approved
        return
    approvers = await User.find(
        User.organization_id == invoice.organization_id,
        User.role == UserRole.approver,
        User.is_deleted == False,
    ).to_list()
    if not approvers:
        approvers = await User.find(
            User.organization_id == invoice.organization_id,
            User.role == UserRole.admin,
            User.is_deleted == False,
        ).to_list()
    invoice.status = InvoiceStatus.pending_approval
    await Approval(
        organization_id=invoice.organization_id,
        invoice_id=str(invoice.id),
        steps=[str(u.id) for u in approvers],
        current_step=0,
        status="pending",
    ).insert()


async def _notify(invoice: Invoice) -> None:
    await hub.broadcast(
        invoice.organization_id,
        {
            "event": "invoice.updated",
            "invoice_id": str(invoice.id),
            "status": invoice.status.value,
        },
    )


class InvoiceService:
    @staticmethod
    async def list_invoices(
        user: User,
        status: InvoiceStatus | None = None,
        vendor: str | None = None,
        department: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[dict], dict]:
        query_conditions: list[Any] = [
            Invoice.organization_id == str(user.organization_id),
            Invoice.is_deleted == False,
        ]
        if status:
            query_conditions.append(Invoice.status == status)
        if vendor:
            query_conditions.append(Invoice.vendor_normalized == normalize_vendor(vendor))
        if department:
            query_conditions.append(Invoice.department == department)
        if date_from:
            query_conditions.append(Invoice.invoice_date >= date_from)
        if date_to:
            query_conditions.append(Invoice.invoice_date <= date_to)

        total = await Invoice.find(*query_conditions).count()
        skip = (page - 1) * limit
        invoices = await Invoice.find(*query_conditions).sort(-Invoice.created_at).skip(skip).limit(limit).to_list()

        total_pages = (total + limit - 1) // limit if total > 0 else 1
        pagination = {
            "total": total,
            "page": page,
            "limit": limit,
            "totalPages": total_pages,
        }
        return [format_invoice(i) for i in invoices], pagination

    @staticmethod
    async def get_invoice(invoice_id: str, user: User) -> Invoice:
        invoice = await Invoice.get(invoice_id)
        assert_org_access(invoice, str(user.organization_id))
        return invoice

    @staticmethod
    async def update_extraction(
        invoice_id: str,
        user: User,
        data: dict[str, Any],
    ) -> Invoice:
        invoice = await InvoiceService.get_invoice(invoice_id, user)
        before = format_invoice(invoice)

        if data.get("vendor_name") is not None:
            invoice.vendor_name = data["vendor_name"].strip()
            invoice.vendor_normalized = normalize_vendor(invoice.vendor_name)
        if data.get("invoice_number") is not None:
            invoice.invoice_number = data["invoice_number"].strip()
        if data.get("invoice_date") is not None:
            invoice.invoice_date = data["invoice_date"].strip()
        if data.get("due_date") is not None:
            invoice.due_date = data["due_date"].strip()
        if data.get("subtotal") is not None:
            invoice.subtotal = data["subtotal"]
        if data.get("tax") is not None:
            invoice.tax = data["tax"]
        if data.get("total") is not None:
            invoice.total = data["total"]
        if data.get("category") is not None:
            invoice.category = data["category"].strip()
            # Store category override for future AI learning
            if invoice.vendor_normalized:
                await CategoryOverride.find_one(
                    CategoryOverride.organization_id == str(user.organization_id),
                    CategoryOverride.vendor_normalized == invoice.vendor_normalized,
                ).upsert(
                    {"$set": {"category": invoice.category}},
                    on_insert=CategoryOverride(
                        organization_id=str(user.organization_id),
                        vendor_normalized=invoice.vendor_normalized,
                        category=invoice.category,
                    ),
                )
        if data.get("department") is not None:
            invoice.department = data["department"].strip()
        if data.get("line_items") is not None:
            invoice.line_items = [
                LineItem(**i) if isinstance(i, dict) else i for i in data["line_items"]
            ]
        if data.get("override_reason") is not None:
            invoice.override_reason = data["override_reason"].strip()

        # Mark confidences as accepted (1.0) since human reviewed
        invoice.field_confidences = {k: 1.0 for k in invoice.field_confidences}

        # Re-validate
        validation = validate_invoice(
            {
                "vendor_name": invoice.vendor_name,
                "total": invoice.total,
                "invoice_date": invoice.invoice_date,
                "subtotal": invoice.subtotal,
                "tax": invoice.tax,
                "line_items": [i.model_dump() for i in invoice.line_items],
            }
        )

        if not validation["ok"]:
            invoice.status = InvoiceStatus.needs_review
        else:
            # Resolve existing missing_fields exception
            exceptions = await InvoiceException.find(
                InvoiceException.invoice_id == str(invoice.id),
                InvoiceException.type == "missing_fields",
                InvoiceException.status == "open",
            ).to_list()
            for ex in exceptions:
                ex.status = "resolved"
                ex.notes = f"Resolved via manual extraction update by user {user.id}"
                await ex.save()

            invoice.status = InvoiceStatus.validated
            await _open_approval(invoice)

        invoice.updated_at = utcnow()
        await invoice.save()

        await write_audit(
            organization_id=str(user.organization_id),
            actor_id=str(user.id),
            action="invoice.extraction_updated",
            resource_type="invoice",
            resource_id=str(invoice.id),
            before=before,
            after=format_invoice(invoice),
        )
        await _notify(invoice)
        return invoice

    @staticmethod
    async def delete_invoice(invoice_id: str, user: User) -> None:
        invoice = await InvoiceService.get_invoice(invoice_id, user)
        invoice.is_deleted = True
        invoice.updated_at = utcnow()
        await invoice.save()

        await write_audit(
            organization_id=str(user.organization_id),
            actor_id=str(user.id),
            action="invoice.deleted",
            resource_type="invoice",
            resource_id=str(invoice.id),
        )
