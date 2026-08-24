from datetime import datetime

from pydantic import BaseModel, Field


class ApprovalDecisionRequest(BaseModel):
    decision: str = Field(pattern="^(approve|reject)$")
    comment: str = ""


class ApprovalItemResponse(BaseModel):
    id: str
    organization_id: str
    invoice_id: str
    status: str
    mode: str
    steps: list[str]
    current_step: int
    decided_by: str | None
    comment: str
    created_at: datetime
    invoice: dict | None = None
