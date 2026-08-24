from typing import Any

from app.core.errors import AppError


def assert_org_access(doc: Any, organization_id: str) -> Any:
    if doc is None or getattr(doc, "is_deleted", False):
        raise AppError("NOT_FOUND", "Resource not found", 404)
    if str(getattr(doc, "organization_id", "")) != str(organization_id):
        raise AppError("NOT_FOUND", "Resource not found", 404)
    return doc
