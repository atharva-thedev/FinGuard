from datetime import UTC, datetime

from app.models.documents import AuditLog


async def write_audit(
    *,
    organization_id: str,
    actor_id: str,
    action: str,
    resource_type: str,
    resource_id: str,
    before: dict | None = None,
    after: dict | None = None,
) -> None:
    await AuditLog(
        organization_id=organization_id,
        actor_id=actor_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        before=before,
        after=after,
        created_at=datetime.now(UTC),
    ).insert()
