from pydantic import BaseModel, Field


class CategoryCreateRequest(BaseModel):
    name: str = Field(min_length=1)


class CategoryResponse(BaseModel):
    id: str
    organization_id: str
    name: str


class CategoryOverrideCreateRequest(BaseModel):
    vendor_name: str = Field(min_length=1)
    category: str = Field(min_length=1)


class CategoryOverrideResponse(BaseModel):
    id: str
    organization_id: str
    vendor_normalized: str
    category: str
