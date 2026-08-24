from fastapi import APIRouter, Depends

from app.core.responses import ok
from app.middleware.auth import require_auth
from app.middleware.role_guard import require_roles
from app.models.documents import User, UserRole
from app.modules.approvals.schemas import ApprovalDecisionRequest
from app.modules.approvals.service import ApprovalService

router = APIRouter(prefix="/approvals", tags=["Approvals"])


@router.get("/pending", dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller, UserRole.approver))])
async def list_pending_approvals(user: User = Depends(require_auth)):
    approvals = await ApprovalService.list_pending(user)
    return ok(approvals)


@router.post("/{approval_id}/decide", dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller, UserRole.approver))])
async def decide_approval(
    approval_id: str,
    payload: ApprovalDecisionRequest,
    user: User = Depends(require_auth),
):
    result = await ApprovalService.decide(
        user=user,
        approval_id=approval_id,
        decision=payload.decision,
        comment=payload.comment,
    )
    return ok(result)


@router.get("/action/{token}")
async def decide_via_action_token(token: str):
    result = await ApprovalService.decide_via_action_token(token)
    return ok(result)
