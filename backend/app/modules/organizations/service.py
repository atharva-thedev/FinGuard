from app.core.errors import AppError
from app.models.documents import Organization, User
from app.utils.audit import write_audit


class OrganizationService:
    @staticmethod
    async def get_org(org_id: str) -> Organization:
        org = await Organization.get(org_id)
        if not org or org.is_deleted:
            raise AppError("NOT_FOUND", "Organization not found", 404)
        return org

    @staticmethod
    async def update_org(
        actor: User,
        name: str | None,
        approval_threshold: float | None,
    ) -> Organization:
        org = await OrganizationService.get_org(str(actor.organization_id))
        before = {
            "name": org.name,
            "approval_threshold": org.approval_threshold,
        }

        if name is not None:
            org.name = name.strip()
        if approval_threshold is not None:
            org.approval_threshold = approval_threshold
        await org.save()

        await write_audit(
            organization_id=str(org.id),
            actor_id=str(actor.id),
            action="organization.updated",
            resource_type="organization",
            resource_id=str(org.id),
            before=before,
            after={
                "name": org.name,
                "approval_threshold": org.approval_threshold,
            },
        )
        return org
