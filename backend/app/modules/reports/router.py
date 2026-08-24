from fastapi import APIRouter, Depends, Query

from app.core.responses import ok
from app.middleware.auth import require_auth
from app.middleware.role_guard import require_roles
from app.models.documents import User, UserRole
from app.modules.reports.service import ReportService

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/spend-summary", dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller, UserRole.viewer))])
async def get_spend_summary(
    month: str | None = Query(None, description="Format YYYY-MM"),
    user: User = Depends(require_auth),
):
    data = await ReportService.get_spend_summary(user, month)
    return ok(data)


@router.get("/budget-vs-actual", dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller, UserRole.viewer))])
async def get_budget_vs_actual(
    month: str | None = Query(None, description="Format YYYY-MM"),
    user: User = Depends(require_auth),
):
    data = await ReportService.get_budget_vs_actual(user, month)
    return ok(data)


@router.get("/dashboard-stats")
async def get_dashboard_stats(user: User = Depends(require_auth)):
    data = await ReportService.get_dashboard_stats(user)
    return ok(data)
