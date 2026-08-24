from collections import defaultdict
from app.models.documents import (
    Approval,
    BudgetRule,
    Invoice,
    InvoiceException,
    InvoiceStatus,
    User,
)
from app.utils.datetime import utcnow


class ReportService:
    @staticmethod
    async def get_spend_summary(user: User, month: str | None = None) -> dict:
        target_month = month or utcnow().strftime("%Y-%m")

        invoices = await Invoice.find(
            Invoice.organization_id == str(user.organization_id),
            Invoice.status == InvoiceStatus.approved,
            Invoice.is_deleted == False,
        ).to_list()

        # Filter to target month
        month_invoices = [
            i for i in invoices
            if (i.invoice_date and i.invoice_date[:7] == target_month)
            or i.created_at.strftime("%Y-%m") == target_month
        ]

        total_spend = sum(float(i.total or 0) for i in month_invoices)

        by_vendor = defaultdict(lambda: {"amount": 0.0, "count": 0})
        by_dept = defaultdict(lambda: {"amount": 0.0, "count": 0})
        by_cat = defaultdict(lambda: {"amount": 0.0, "count": 0})

        for i in month_invoices:
            amt = float(i.total or 0)
            v = i.vendor_name or "Unknown Vendor"
            d = i.department or "General"
            c = i.category or "Other"

            by_vendor[v]["amount"] += amt
            by_vendor[v]["count"] += 1

            by_dept[d]["amount"] += amt
            by_dept[d]["count"] += 1

            by_cat[c]["amount"] += amt
            by_cat[c]["count"] += 1

        return {
            "total_spend": round(total_spend, 2),
            "month": target_month,
            "spend_by_vendor": [
                {"name": k, "amount": round(v["amount"], 2), "invoice_count": v["count"]}
                for k, v in sorted(by_vendor.items(), key=lambda item: item[1]["amount"], reverse=True)
            ],
            "spend_by_department": [
                {"name": k, "amount": round(v["amount"], 2), "invoice_count": v["count"]}
                for k, v in sorted(by_dept.items(), key=lambda item: item[1]["amount"], reverse=True)
            ],
            "spend_by_category": [
                {"name": k, "amount": round(v["amount"], 2), "invoice_count": v["count"]}
                for k, v in sorted(by_cat.items(), key=lambda item: item[1]["amount"], reverse=True)
            ],
        }

    @staticmethod
    async def get_budget_vs_actual(user: User, month: str | None = None) -> list[dict]:
        target_month = month or utcnow().strftime("%Y-%m")

        budgets = await BudgetRule.find(
            BudgetRule.organization_id == str(user.organization_id),
            BudgetRule.is_deleted == False,
        ).to_list()

        invoices = await Invoice.find(
            Invoice.organization_id == str(user.organization_id),
            Invoice.status == InvoiceStatus.approved,
            Invoice.is_deleted == False,
        ).to_list()

        month_invoices = [
            i for i in invoices
            if (i.invoice_date and i.invoice_date[:7] == target_month)
            or i.created_at.strftime("%Y-%m") == target_month
        ]

        actual_spend_map = defaultdict(float)
        for i in month_invoices:
            key = (i.department or "General", i.category or "Other")
            actual_spend_map[key] += float(i.total or 0)

        results = []
        for b in budgets:
            actual = actual_spend_map.get((b.department, b.category), 0.0)
            variance = b.monthly_limit - actual
            pct = (actual / b.monthly_limit * 100) if b.monthly_limit > 0 else 0.0

            results.append({
                "department": b.department,
                "category": b.category,
                "monthly_limit": round(b.monthly_limit, 2),
                "actual_spend": round(actual, 2),
                "variance": round(variance, 2),
                "percentage_used": round(pct, 1),
            })
        return results

    @staticmethod
    async def get_dashboard_stats(user: User) -> dict:
        now_month = utcnow().strftime("%Y-%m")
        org_id = str(user.organization_id)

        all_invoices = await Invoice.find(
            Invoice.organization_id == org_id,
            Invoice.is_deleted == False,
        ).to_list()

        pending_approvals = await Approval.find(
            Approval.organization_id == org_id,
            Approval.status == "pending",
            Approval.is_deleted == False,
        ).count()

        open_exceptions = await InvoiceException.find(
            InvoiceException.organization_id == org_id,
            InvoiceException.status == "open",
            InvoiceException.is_deleted == False,
        ).count()

        month_spend = 0.0
        needs_review_count = 0
        approved_count = 0

        for inv in all_invoices:
            if inv.status == InvoiceStatus.needs_review:
                needs_review_count += 1
            elif inv.status == InvoiceStatus.approved:
                approved_count += 1
                if (inv.invoice_date and inv.invoice_date[:7] == now_month) or inv.created_at.strftime("%Y-%m") == now_month:
                    month_spend += float(inv.total or 0)

        return {
            "total_spend_month": round(month_spend, 2),
            "month": now_month,
            "pending_approvals_count": pending_approvals,
            "needs_review_count": needs_review_count,
            "open_exceptions_count": open_exceptions,
            "approved_invoices_count": approved_count,
            "total_invoices_count": len(all_invoices),
        }
