from app.core.errors import AppError
from app.domain.invoice_rules import normalize_vendor
from app.models.documents import Category, CategoryOverride, User


class CategoryService:
    @staticmethod
    async def list_categories(user: User) -> list[dict]:
        cats = await Category.find(
            Category.organization_id == str(user.organization_id),
            Category.is_deleted == False,
        ).to_list()
        return [{"id": str(c.id), "organization_id": str(c.organization_id), "name": c.name} for c in cats]

    @staticmethod
    async def create_category(user: User, name: str) -> Category:
        name_clean = name.strip()
        existing = await Category.find_one(
            Category.organization_id == str(user.organization_id),
            Category.name == name_clean,
            Category.is_deleted == False,
        )
        if existing:
            raise AppError("CATEGORY_ALREADY_EXISTS", f"Category '{name_clean}' already exists", 409)

        cat = Category(organization_id=str(user.organization_id), name=name_clean)
        await cat.insert()
        return cat

    @staticmethod
    async def list_overrides(user: User) -> list[dict]:
        overrides = await CategoryOverride.find(
            CategoryOverride.organization_id == str(user.organization_id),
        ).to_list()
        return [
            {
                "id": str(o.id),
                "organization_id": str(o.organization_id),
                "vendor_normalized": o.vendor_normalized,
                "category": o.category,
            }
            for o in overrides
        ]

    @staticmethod
    async def set_override(user: User, vendor_name: str, category: str) -> CategoryOverride:
        norm = normalize_vendor(vendor_name)
        existing = await CategoryOverride.find_one(
            CategoryOverride.organization_id == str(user.organization_id),
            CategoryOverride.vendor_normalized == norm,
        )
        if existing:
            existing.category = category.strip()
            await existing.save()
            return existing

        override = CategoryOverride(
            organization_id=str(user.organization_id),
            vendor_normalized=norm,
            category=category.strip(),
        )
        await override.insert()
        return override
