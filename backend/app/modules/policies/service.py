from typing import Any

from app.models.documents import BudgetRule, PolicyRule, User
from app.utils.audit import write_audit
from app.utils.ownership import assert_org_access


def format_budget(b: BudgetRule) -> dict:
    return {
        "id": str(b.id),
        "organization_id": str(b.organization_id),
        "department": b.department,
        "category": b.category,
        "monthly_limit": b.monthly_limit,
    }


def format_policy(p: PolicyRule) -> dict:
    return {
        "id": str(p.id),
        "organization_id": str(p.organization_id),
        "code": p.code,
        "enabled": p.enabled,
        "config": p.config,
    }


class PolicyService:
    @staticmethod
    async def list_budgets(user: User) -> list[dict]:
        rules = await BudgetRule.find(
            BudgetRule.organization_id == str(user.organization_id),
            BudgetRule.is_deleted == False,
        ).to_list()
        return [format_budget(r) for r in rules]

    @staticmethod
    async def create_budget(
        user: User,
        department: str,
        category: str,
        monthly_limit: float,
    ) -> BudgetRule:
        existing = await BudgetRule.find_one(
            BudgetRule.organization_id == str(user.organization_id),
            BudgetRule.department == department.strip(),
            BudgetRule.category == category.strip(),
            BudgetRule.is_deleted == False,
        )
        if existing:
            existing.monthly_limit = monthly_limit
            await existing.save()
            return existing

        rule = BudgetRule(
            organization_id=str(user.organization_id),
            department=department.strip(),
            category=category.strip(),
            monthly_limit=monthly_limit,
        )
        await rule.insert()

        await write_audit(
            organization_id=str(user.organization_id),
            actor_id=str(user.id),
            action="budget_rule.created",
            resource_type="budget_rule",
            resource_id=str(rule.id),
            after={"department": rule.department, "category": rule.category, "limit": monthly_limit},
        )
        return rule

    @staticmethod
    async def update_budget(
        user: User,
        budget_id: str,
        monthly_limit: float,
    ) -> BudgetRule:
        rule = await BudgetRule.get(budget_id)
        assert_org_access(rule, str(user.organization_id))

        before = {"monthly_limit": rule.monthly_limit}
        rule.monthly_limit = monthly_limit
        await rule.save()

        await write_audit(
            organization_id=str(user.organization_id),
            actor_id=str(user.id),
            action="budget_rule.updated",
            resource_type="budget_rule",
            resource_id=str(rule.id),
            before=before,
            after={"monthly_limit": monthly_limit},
        )
        return rule

    @staticmethod
    async def delete_budget(user: User, budget_id: str) -> None:
        rule = await BudgetRule.get(budget_id)
        assert_org_access(rule, str(user.organization_id))
        rule.is_deleted = True
        await rule.save()

        await write_audit(
            organization_id=str(user.organization_id),
            actor_id=str(user.id),
            action="budget_rule.deleted",
            resource_type="budget_rule",
            resource_id=str(rule.id),
        )

    @staticmethod
    async def list_policy_rules(user: User) -> list[dict]:
        rules = await PolicyRule.find(
            PolicyRule.organization_id == str(user.organization_id),
            PolicyRule.is_deleted == False,
        ).to_list()
        return [format_policy(r) for r in rules]

    @staticmethod
    async def update_policy_rule(
        user: User,
        code: str,
        enabled: bool,
        config: dict[str, Any] | None,
    ) -> PolicyRule:
        rule = await PolicyRule.find_one(
            PolicyRule.organization_id == str(user.organization_id),
            PolicyRule.code == code,
            PolicyRule.is_deleted == False,
        )
        if not rule:
            rule = PolicyRule(
                organization_id=str(user.organization_id),
                code=code,
                enabled=enabled,
                config=config or {},
            )
            await rule.insert()
        else:
            before = {"enabled": rule.enabled, "config": rule.config}
            rule.enabled = enabled
            if config is not None:
                rule.config = config
            await rule.save()

            await write_audit(
                organization_id=str(user.organization_id),
                actor_id=str(user.id),
                action="policy_rule.updated",
                resource_type="policy_rule",
                resource_id=str(rule.id),
                before=before,
                after={"enabled": rule.enabled, "config": rule.config},
            )
        return rule
