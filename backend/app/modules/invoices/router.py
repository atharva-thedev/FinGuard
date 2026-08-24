from fastapi import APIRouter, Depends, File, Form, Query, UploadFile

from app.core.responses import ok
from app.middleware.auth import require_auth
from app.middleware.role_guard import require_roles
from app.models.documents import InvoiceStatus, User, UserRole
from app.modules.invoices.schemas import UpdateExtractionRequest
from app.modules.invoices.service import (
    InvoiceService,
    create_from_uploads,
    format_invoice,
    run_pipeline,
)

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("", status_code=201, dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller, UserRole.ap_clerk))])
async def upload_invoices(
    files: list[UploadFile] = File(...),
    department: str = Form(""),
    user: User = Depends(require_auth),
):
    created = await create_from_uploads(user=user, files=files, department=department)
    return ok([format_invoice(i) for i in created], status_code=201)


@router.get("")
async def list_invoices(
    status: InvoiceStatus | None = Query(None),
    vendor: str | None = Query(None),
    department: str | None = Query(None),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: User = Depends(require_auth),
):
    invoices, pagination = await InvoiceService.list_invoices(
        user=user,
        status=status,
        vendor=vendor,
        department=department,
        date_from=date_from,
        date_to=date_to,
        page=page,
        limit=limit,
    )
    return ok(invoices, pagination=pagination)


@router.get("/{invoice_id}")
async def get_invoice(
    invoice_id: str,
    user: User = Depends(require_auth),
):
    invoice = await InvoiceService.get_invoice(invoice_id, user)
    return ok(format_invoice(invoice))


@router.patch("/{invoice_id}/extraction", dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller, UserRole.ap_clerk))])
async def update_extraction(
    invoice_id: str,
    payload: UpdateExtractionRequest,
    user: User = Depends(require_auth),
):
    updated = await InvoiceService.update_extraction(
        invoice_id=invoice_id,
        user=user,
        data=payload.model_dump(exclude_unset=True),
    )
    return ok(format_invoice(updated))


@router.post("/{invoice_id}/reprocess", dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller, UserRole.ap_clerk))])
async def reprocess_invoice(
    invoice_id: str,
    user: User = Depends(require_auth),
):
    # Verify access first
    await InvoiceService.get_invoice(invoice_id, user)
    reprocessed = await run_pipeline(invoice_id, actor_id=str(user.id))
    return ok(format_invoice(reprocessed))


@router.delete("/{invoice_id}", dependencies=[Depends(require_roles(UserRole.admin))])
async def delete_invoice(
    invoice_id: str,
    user: User = Depends(require_auth),
):
    await InvoiceService.delete_invoice(invoice_id, user)
    return ok({"message": "Invoice deleted"})
