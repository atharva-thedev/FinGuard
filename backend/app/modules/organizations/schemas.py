from datetime import datetime

from pydantic import BaseModel, Field


class OrganizationResponse(BaseModel):
    id: str
    name: str
    slug: str
    approval_threshold: float
    created_at: datetime


class UpdateOrganizationRequest(BaseModel):
    name: str | None = Field(None, min_length=1)
    approval_threshold: float | None = Field(None, ge=0)
