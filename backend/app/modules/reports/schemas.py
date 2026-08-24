from pydantic import BaseModel


class SpendItem(BaseModel):
    name: str
    amount: float
    invoice_count: int


class SpendSummaryResponse(BaseModel):
    total_spend: float
    month: str
    spend_by_vendor: list[SpendItem]
    spend_by_department: list[SpendItem]
    spend_by_category: list[SpendItem]


class BudgetVsActualItem(BaseModel):
    department: str
    category: str
    monthly_limit: float
    actual_spend: float
    variance: float
    percentage_used: float


class DashboardStatsResponse(BaseModel):
    total_spend_month: float
    month: str
    pending_approvals_count: int
    needs_review_count: int
    open_exceptions_count: int
    approved_invoices_count: int
    total_invoices_count: int
