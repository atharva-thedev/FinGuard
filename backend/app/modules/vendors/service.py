from app.core.errors import AppError
from app.domain.invoice_rules import normalize_vendor
from app.models.documents import User, Vendor
from app.utils.audit import write_audit
from app.utils.ownership import assert_org_access


def format_vendor(v: Vendor) -> dict:
    return {
        "id": str(v.id),
        "organization_id": str(v.organization_id),
        "name": v.name,
        "normalized_name": v.normalized_name,
        "registered": v.registered,
        "created_at": v.created_at,
    }


class VendorService:
    @staticmethod
    async def list_vendors(user: User, search: str | None = None) -> list[dict]:
        query = [
            Vendor.organization_id == str(user.organization_id),
            Vendor.is_deleted == False,
        ]
        vendors = await Vendor.find(*query).sort(Vendor.name).to_list()
        if search:
            s = search.strip().lower()
            vendors = [v for v in vendors if s in v.name.lower()]
        return [format_vendor(v) for v in vendors]

    @staticmethod
    async def create_vendor(user: User, name: str, registered: bool = True) -> Vendor:
        norm = normalize_vendor(name)
        existing = await Vendor.find_one(
            Vendor.organization_id == str(user.organization_id),
            Vendor.normalized_name == norm,
            Vendor.is_deleted == False,
        )
        if existing:
            raise AppError("VENDOR_ALREADY_EXISTS", f"Vendor '{name}' already exists in your organization", 409)

        vendor = Vendor(
            organization_id=str(user.organization_id),
            name=name.strip(),
            normalized_name=norm,
            registered=registered,
        )
        await vendor.insert()

        await write_audit(
            organization_id=str(user.organization_id),
            actor_id=str(user.id),
            action="vendor.created",
            resource_type="vendor",
            resource_id=str(vendor.id),
            after={"name": vendor.name, "registered": vendor.registered},
        )
        return vendor

    @staticmethod
    async def update_vendor(
        user: User,
        vendor_id: str,
        name: str | None,
        registered: bool | None,
    ) -> Vendor:
        vendor = await Vendor.get(vendor_id)
        assert_org_access(vendor, str(user.organization_id))

        before = {"name": vendor.name, "registered": vendor.registered}
        if name is not None:
            norm = normalize_vendor(name)
            if norm != vendor.normalized_name:
                existing = await Vendor.find_one(
                    Vendor.organization_id == str(user.organization_id),
                    Vendor.normalized_name == norm,
                    Vendor.id != vendor.id,
                    Vendor.is_deleted == False,
                )
                if existing:
                    raise AppError("CONFLICT", f"Vendor '{name}' already exists", 409)
            vendor.name = name.strip()
            vendor.normalized_name = norm
        if registered is not None:
            vendor.registered = registered
        await vendor.save()

        await write_audit(
            organization_id=str(user.organization_id),
            actor_id=str(user.id),
            action="vendor.updated",
            resource_type="vendor",
            resource_id=str(vendor.id),
            before=before,
            after={"name": vendor.name, "registered": vendor.registered},
        )
        return vendor

    @staticmethod
    async def delete_vendor(user: User, vendor_id: str) -> None:
        vendor = await Vendor.get(vendor_id)
        assert_org_access(vendor, str(user.organization_id))
        vendor.is_deleted = True
        await vendor.save()

        await write_audit(
            organization_id=str(user.organization_id),
            actor_id=str(user.id),
            action="vendor.deleted",
            resource_type="vendor",
            resource_id=str(vendor.id),
        )
