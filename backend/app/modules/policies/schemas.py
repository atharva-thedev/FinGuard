from typing import Any

from pydantic import BaseModel, Field


class BudgetRuleCreateRequest(BaseModel):
    department: str = Field(min_length=1)
    category: str = Field(min_length=1)
    monthly_limit: float = Field(gt=0)


class BudgetRuleUpdateRequest(BaseModel):
    monthly_limit: float = Field(gt=0)


class BudgetRuleResponse(BaseModel):
    id: str
    organization_id: str
    department: str
    category: str
    monthly_limit: float


class PolicyRuleUpdateRequest(BaseModel):
    enabled: bool
    config: dict[str, Any] | None = None


class PolicyRuleResponse(BaseModel):
    id: str
    organization_id: str
    code: str
    enabled: bool
    config: dict[str, Any]
