from datetime import UTC, datetime

from app.core.errors import AppError
from app.models.documents import Approval, Invoice, InvoiceStatus, User, UserRole
from app.modules.invoices.service import format_invoice
from app.realtime.hub import hub
from app.utils.audit import write_audit
from app.utils.datetime import utcnow
from app.utils.jwt import verify_email_action
from app.utils.ownership import assert_org_access


def format_approval(appr: Approval, invoice: Invoice | None = None) -> dict:
    return {
        "id": str(appr.id),
        "organization_id": str(appr.organization_id),
        "invoice_id": str(appr.invoice_id),
        "status": appr.status,
        "mode": appr.mode.value,
        "steps": appr.steps,
        "current_step": appr.current_step,
        "decided_by": appr.decided_by,
        "comment": appr.comment,
        "created_at": appr.created_at,
        "invoice": format_invoice(invoice) if invoice else None,
    }


class ApprovalService:
    @staticmethod
    async def list_pending(user: User) -> list[dict]:
        approvals = await Approval.find(
            Approval.organization_id == str(user.organization_id),
            Approval.status == "pending",
            Approval.is_deleted == False,
        ).sort(-Approval.created_at).to_list()

        results = []
        user_id_str = str(user.id)
        for a in approvals:
            # Check if current user is the current assigned approver, in steps, or admin
            is_assigned = (
                user.role == UserRole.admin
                or (a.steps and a.current_step < len(a.steps) and a.steps[a.current_step] == user_id_str)
                or user_id_str in a.steps
            )
            if is_assigned:
                inv = await Invoice.get(a.invoice_id)
                results.append(format_approval(a, inv))
        return results

    @staticmethod
    async def decide(
        user: User,
        approval_id: str,
        decision: str,
        comment: str = "",
    ) -> dict:
        approval = await Approval.get(approval_id)
        assert_org_access(approval, str(user.organization_id))

        if approval.status != "pending":
            raise AppError("INVALID_REQUEST", f"Approval is already {approval.status}", 400)

        invoice = await Invoice.get(approval.invoice_id)
        if not invoice or invoice.is_deleted:
            raise AppError("NOT_FOUND", "Invoice not found", 404)

        before_status = approval.status
        approval.decided_by = str(user.id)
        approval.comment = comment

        if decision == "approve":
            approval.status = "approved"
            invoice.status = InvoiceStatus.approved
        else:
            approval.status = "rejected"
            invoice.status = InvoiceStatus.rejected

        await approval.save()
        invoice.updated_at = utcnow()
        await invoice.save()

        await write_audit(
            organization_id=str(user.organization_id),
            actor_id=str(user.id),
            action=f"approval.{decision}d",
            resource_type="approval",
            resource_id=str(approval.id),
            before={"status": before_status},
            after={"status": approval.status, "comment": comment, "invoice_id": str(invoice.id)},
        )

        await hub.broadcast(
            str(user.organization_id),
            {
                "event": "invoice.updated",
                "invoice_id": str(invoice.id),
                "status": invoice.status.value,
            },
        )
        return format_approval(approval, invoice)

    @staticmethod
    async def decide_via_action_token(token: str) -> dict:
        return await ApprovalService.decide_by_action_token(token)

    @staticmethod
    async def decide_by_action_token(token: str) -> dict:
        payload = verify_email_action(token)
        approval_id = payload.get("sub")
        action = payload.get("act")

        approval = await Approval.get(approval_id)
        if not approval or approval.is_deleted:
            raise AppError("NOT_FOUND", "Approval request not found", 404)

        if approval.status != "pending":
            raise AppError("INVALID_REQUEST", f"Approval has already been resolved ({approval.status})", 400)

        invoice = await Invoice.get(approval.invoice_id)
        if not invoice or invoice.is_deleted:
            raise AppError("NOT_FOUND", "Invoice not found", 404)

        approval.decided_by = "email_action_link"
        approval.comment = "Decided via email 1-click action link"

        if action == "approve":
            approval.status = "approved"
            invoice.status = InvoiceStatus.approved
        else:
            approval.status = "rejected"
            invoice.status = InvoiceStatus.rejected

        await approval.save()
        invoice.updated_at = utcnow()
        await invoice.save()

        await write_audit(
            organization_id=str(approval.organization_id),
            actor_id="system.email_action",
            action=f"approval.{action}d",
            resource_type="approval",
            resource_id=str(approval.id),
            after={"status": approval.status, "invoice_id": str(invoice.id)},
        )

        await hub.broadcast(
            str(approval.organization_id),
            {
                "event": "invoice.updated",
                "invoice_id": str(invoice.id),
                "status": invoice.status.value,
            },
        )
        return {"status": approval.status, "invoice_id": str(invoice.id), "message": f"Invoice successfully {approval.status}"}
