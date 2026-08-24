from typing import Any

from app.models.documents import AuditLog, User


def format_audit(a: AuditLog) -> dict:
    return {
        "id": str(a.id),
        "organization_id": str(a.organization_id),
        "actor_id": str(a.actor_id),
        "action": a.action,
        "resource_type": a.resource_type,
        "resource_id": str(a.resource_id),
        "before": a.before,
        "after": a.after,
        "created_at": a.created_at,
    }


class AuditService:
    @staticmethod
    async def list_logs(
        user: User,
        resource_type: str | None = None,
        actor_id: str | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> tuple[list[dict], dict]:
        query_conditions: list[Any] = [AuditLog.organization_id == str(user.organization_id)]
        if resource_type:
            query_conditions.append(AuditLog.resource_type == resource_type)
        if actor_id:
            query_conditions.append(AuditLog.actor_id == actor_id)

        total = await AuditLog.find(*query_conditions).count()
        skip = (page - 1) * limit
        logs = await AuditLog.find(*query_conditions).sort(-AuditLog.created_at).skip(skip).limit(limit).to_list()

        total_pages = (total + limit - 1) // limit if total > 0 else 1
        pagination = {
            "total": total,
            "page": page,
            "limit": limit,
            "totalPages": total_pages,
        }
        return [format_audit(a) for a in logs], pagination
