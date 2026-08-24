from datetime import UTC, datetime

from app.core.errors import AppError
from app.models.documents import (
    ExceptionType,
    Invoice,
    InvoiceException,
    InvoiceStatus,
    User,
    UserRole,
)
from app.modules.invoices.service import _open_approval, format_invoice, run_pipeline
from app.realtime.hub import hub
from app.utils.audit import write_audit
from app.utils.datetime import utcnow
from app.utils.ownership import assert_org_access


def format_exception(exc: InvoiceException, invoice: Invoice | None = None) -> dict:
    return {
        "id": str(exc.id),
        "organization_id": str(exc.organization_id),
        "invoice_id": str(exc.invoice_id),
        "type": exc.type.value if isinstance(exc.type, ExceptionType) else str(exc.type),
        "status": exc.status,
        "notes": exc.notes,
        "created_at": exc.created_at,
        "invoice": format_invoice(invoice) if invoice else None,
    }


class ExceptionService:
    @staticmethod
    async def list_exceptions(
        user: User,
        type_filter: str | None = None,
        status_filter: str | None = "open",
    ) -> list[dict]:
        query = [
            InvoiceException.organization_id == str(user.organization_id),
            InvoiceException.is_deleted == False,
        ]
        if status_filter:
            query.append(InvoiceException.status == status_filter)
        if type_filter:
            query.append(InvoiceException.type == type_filter)

        exceptions = await InvoiceException.find(*query).sort(-InvoiceException.created_at).to_list()
        results = []
        for e in exceptions:
            inv = await Invoice.get(e.invoice_id)
            results.append(format_exception(e, inv))
        return results

    @staticmethod
    async def resolve(
        user: User,
        exception_id: str,
        action: str,
        notes: str,
    ) -> dict:
        exception = await InvoiceException.get(exception_id)
        assert_org_access(exception, str(user.organization_id))

        if exception.status == "resolved":
            raise AppError("INVALID_REQUEST", "Exception is already resolved", 400)

        # Role checks per PRD §7 SLA / Exception table
        etype = exception.type.value if isinstance(exception.type, ExceptionType) else str(exception.type)
        if etype in ("policy", "budget") and user.role not in (UserRole.admin, UserRole.controller):
            raise AppError("FORBIDDEN", "Only Controllers and Admins can resolve policy or budget exceptions", 403)

        invoice = await Invoice.get(exception.invoice_id)
        if not invoice or invoice.is_deleted:
            raise AppError("NOT_FOUND", "Associated invoice not found", 404)

        exception.status = "resolved"
        exception.notes = f"{exception.notes} | Resolution by {user.full_name}: {notes}".strip(" |")
        await exception.save()

        if action == "reprocess":
            await run_pipeline(str(invoice.id), actor_id=str(user.id))
        elif action == "force_validate":
            invoice.override_reason = notes
            invoice.status = InvoiceStatus.validated
            invoice.updated_at = utcnow()
            await invoice.save()
            await _open_approval(invoice)
            await invoice.save()
        elif action == "reject":
            invoice.status = InvoiceStatus.rejected
            invoice.override_reason = notes
            invoice.updated_at = utcnow()
            await invoice.save()

        await write_audit(
            organization_id=str(user.organization_id),
            actor_id=str(user.id),
            action="exception.resolved",
            resource_type="exception",
            resource_id=str(exception.id),
            after={"action": action, "notes": notes, "invoice_id": str(invoice.id)},
        )

        await hub.broadcast(
            str(user.organization_id),
            {
                "event": "invoice.updated",
                "invoice_id": str(invoice.id),
                "status": invoice.status.value,
            },
        )
        return format_exception(exception, invoice)
