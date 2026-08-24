from fastapi import APIRouter, Depends

from app.core.responses import ok
from app.middleware.auth import require_auth
from app.middleware.role_guard import require_roles
from app.models.documents import User, UserRole
from app.modules.categories.schemas import (
    CategoryCreateRequest,
    CategoryOverrideCreateRequest,
)
from app.modules.categories.service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("")
async def list_categories(user: User = Depends(require_auth)):
    cats = await CategoryService.list_categories(user)
    return ok(cats)


@router.post("", status_code=201, dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller))])
async def create_category(
    payload: CategoryCreateRequest,
    user: User = Depends(require_auth),
):
    cat = await CategoryService.create_category(user, payload.name)
    return ok({"id": str(cat.id), "organization_id": str(cat.organization_id), "name": cat.name}, status_code=201)


@router.get("/overrides")
async def list_category_overrides(user: User = Depends(require_auth)):
    overrides = await CategoryService.list_overrides(user)
    return ok(overrides)


@router.post("/overrides", status_code=201, dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller, UserRole.ap_clerk))])
async def set_category_override(
    payload: CategoryOverrideCreateRequest,
    user: User = Depends(require_auth),
):
    override = await CategoryService.set_override(user, payload.vendor_name, payload.category)
    return ok(
        {
            "id": str(override.id),
            "organization_id": str(override.organization_id),
            "vendor_normalized": override.vendor_normalized,
            "category": override.category,
        },
        status_code=201,
    )
