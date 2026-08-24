from fastapi import APIRouter, Depends

from app.core.responses import ok
from app.middleware.auth import require_auth
from app.middleware.role_guard import require_roles
from app.models.documents import User, UserRole
from app.modules.policies.schemas import (
    BudgetRuleCreateRequest,
    BudgetRuleUpdateRequest,
    PolicyRuleUpdateRequest,
)
from app.modules.policies.service import PolicyService, format_budget, format_policy

router = APIRouter(prefix="/policies", tags=["Policies"])


@router.get("/budgets")
async def list_budgets(user: User = Depends(require_auth)):
    budgets = await PolicyService.list_budgets(user)
    return ok(budgets)


@router.post("/budgets", status_code=201, dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller))])
async def create_budget(
    payload: BudgetRuleCreateRequest,
    user: User = Depends(require_auth),
):
    rule = await PolicyService.create_budget(
        user=user,
        department=payload.department,
        category=payload.category,
        monthly_limit=payload.monthly_limit,
    )
    return ok(format_budget(rule), status_code=201)


@router.patch("/budgets/{budget_id}", dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller))])
async def update_budget(
    budget_id: str,
    payload: BudgetRuleUpdateRequest,
    user: User = Depends(require_auth),
):
    updated = await PolicyService.update_budget(user, budget_id, payload.monthly_limit)
    return ok(format_budget(updated))


@router.delete("/budgets/{budget_id}", dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller))])
async def delete_budget(
    budget_id: str,
    user: User = Depends(require_auth),
):
    await PolicyService.delete_budget(user, budget_id)
    return ok({"message": "Budget rule deleted"})


@router.get("/rules")
async def list_policy_rules(user: User = Depends(require_auth)):
    rules = await PolicyService.list_policy_rules(user)
    return ok(rules)


@router.patch("/rules/{code}", dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller))])
async def update_policy_rule(
    code: str,
    payload: PolicyRuleUpdateRequest,
    user: User = Depends(require_auth),
):
    updated = await PolicyService.update_policy_rule(user, code, payload.enabled, payload.config)
    return ok(format_policy(updated))
