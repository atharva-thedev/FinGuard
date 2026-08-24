from fastapi import APIRouter, Depends, Query

from app.core.responses import ok
from app.middleware.auth import require_auth
from app.middleware.role_guard import require_roles
from app.models.documents import User, UserRole
from app.modules.audit.service import AuditService

router = APIRouter(prefix="/audit-logs", tags=["Audit"])


@router.get("", dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller, UserRole.viewer))])
async def list_audit_logs(
    resource_type: str | None = Query(None),
    actor_id: str | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    user: User = Depends(require_auth),
):
    logs, pagination = await AuditService.list_logs(
        user=user,
        resource_type=resource_type,
        actor_id=actor_id,
        page=page,
        limit=limit,
    )
    return ok(logs, pagination=pagination)
