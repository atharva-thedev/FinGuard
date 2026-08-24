from datetime import datetime

from pydantic import BaseModel, Field


class VendorCreateRequest(BaseModel):
    name: str = Field(min_length=1)
    registered: bool = True


class VendorUpdateRequest(BaseModel):
    name: str | None = Field(None, min_length=1)
    registered: bool | None = None


class VendorResponse(BaseModel):
    id: str
    organization_id: str
    name: str
    normalized_name: str
    registered: bool
    created_at: datetime
