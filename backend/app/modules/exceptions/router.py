from fastapi import APIRouter, Depends, Query

from app.core.responses import ok
from app.middleware.auth import require_auth
from app.middleware.role_guard import require_roles
from app.models.documents import User, UserRole
from app.modules.exceptions.schemas import ExceptionResolveRequest
from app.modules.exceptions.service import ExceptionService

router = APIRouter(prefix="/exceptions", tags=["Exceptions"])


@router.get("", dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller, UserRole.ap_clerk))])
async def list_exceptions(
    type_filter: str | None = Query(None, alias="type"),
    status: str | None = Query("open"),
    user: User = Depends(require_auth),
):
    exceptions = await ExceptionService.list_exceptions(
        user=user,
        type_filter=type_filter,
        status_filter=status,
    )
    return ok(exceptions)


@router.post("/{exception_id}/resolve", dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller, UserRole.ap_clerk))])
async def resolve_exception(
    exception_id: str,
    payload: ExceptionResolveRequest,
    user: User = Depends(require_auth),
):
    result = await ExceptionService.resolve(
        user=user,
        exception_id=exception_id,
        action=payload.action,
        notes=payload.notes,
    )
    return ok(result)
