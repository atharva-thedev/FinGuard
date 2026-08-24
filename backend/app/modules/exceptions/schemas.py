from datetime import datetime

from pydantic import BaseModel, Field


class ExceptionResolveRequest(BaseModel):
    action: str = Field(pattern="^(force_validate|reprocess|reject)$")
    notes: str = Field(min_length=1)


class ExceptionItemResponse(BaseModel):
    id: str
    organization_id: str
    invoice_id: str
    type: str
    status: str
    notes: str
    created_at: datetime
    invoice: dict | None = None
