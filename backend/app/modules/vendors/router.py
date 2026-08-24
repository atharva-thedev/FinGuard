from fastapi import APIRouter, Depends, Query

from app.core.responses import ok
from app.middleware.auth import require_auth
from app.middleware.role_guard import require_roles
from app.models.documents import User, UserRole
from app.modules.vendors.schemas import VendorCreateRequest, VendorUpdateRequest
from app.modules.vendors.service import VendorService, format_vendor

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.get("")
async def list_vendors(
    search: str | None = Query(None),
    user: User = Depends(require_auth),
):
    vendors = await VendorService.list_vendors(user, search)
    return ok(vendors)


@router.post("", status_code=201, dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller, UserRole.ap_clerk))])
async def create_vendor(
    payload: VendorCreateRequest,
    user: User = Depends(require_auth),
):
    vendor = await VendorService.create_vendor(user, payload.name, payload.registered)
    return ok(format_vendor(vendor), status_code=201)


@router.patch("/{vendor_id}", dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller))])
async def update_vendor(
    vendor_id: str,
    payload: VendorUpdateRequest,
    user: User = Depends(require_auth),
):
    updated = await VendorService.update_vendor(user, vendor_id, payload.name, payload.registered)
    return ok(format_vendor(updated))


@router.delete("/{vendor_id}", dependencies=[Depends(require_roles(UserRole.admin))])
async def delete_vendor(
    vendor_id: str,
    user: User = Depends(require_auth),
):
    await VendorService.delete_vendor(user, vendor_id)
    return ok({"message": "Vendor deleted"})
