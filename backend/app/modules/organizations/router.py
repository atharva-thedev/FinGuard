from fastapi import APIRouter, Depends

from app.core.responses import ok
from app.middleware.auth import require_auth
from app.middleware.role_guard import require_roles
from app.models.documents import Organization, User, UserRole
from app.modules.organizations.schemas import UpdateOrganizationRequest
from app.modules.organizations.service import OrganizationService

router = APIRouter(prefix="/organizations", tags=["Organizations"])


def _format_org(org: Organization) -> dict:
    return {
        "id": str(org.id),
        "name": org.name,
        "slug": org.slug,
        "approval_threshold": org.approval_threshold,
        "created_at": org.created_at,
    }


@router.get("/me")
async def get_my_organization(user: User = Depends(require_auth)):
    org = await OrganizationService.get_org(str(user.organization_id))
    return ok(_format_org(org))


@router.patch("/me", dependencies=[Depends(require_roles(UserRole.admin))])
async def update_my_organization(
    payload: UpdateOrganizationRequest,
    user: User = Depends(require_auth),
):
    updated = await OrganizationService.update_org(
        actor=user,
        name=payload.name,
        approval_threshold=payload.approval_threshold,
    )
    return ok(_format_org(updated))
