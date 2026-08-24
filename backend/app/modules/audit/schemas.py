from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AuditLogItemResponse(BaseModel):
    id: str
    organization_id: str
    actor_id: str
    action: str
    resource_type: str
    resource_id: str
    before: dict[str, Any] | None = None
    after: dict[str, Any] | None = None
    created_at: datetime
