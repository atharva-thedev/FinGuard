from app.core.errors import AppError
from app.core.security import hash_password, verify_password
from app.models.documents import AuditLog, Invoice, Session, User, UserRole
from app.utils.audit import write_audit
from app.utils.datetime import utcnow


class UserService:
    @staticmethod
    async def update_profile(user: User, full_name: str | None, department: str | None) -> User:
        before = {"full_name": user.full_name, "department": user.department}
        if full_name is not None:
            user.full_name = full_name.strip()
        if department is not None:
            user.department = department.strip()
        await user.save()

        await write_audit(
            organization_id=user.organization_id,
            actor_id=str(user.id),
            action="user.updated_profile",
            resource_type="user",
            resource_id=str(user.id),
            before=before,
            after={"full_name": user.full_name, "department": user.department},
        )
        return user

    @staticmethod
    async def change_password(user: User, current_pw: str, new_pw: str) -> None:
        if not user.password_hash or not verify_password(current_pw, user.password_hash):
            raise AppError("INVALID_CURRENT_PASSWORD", "Current password is incorrect", 400)

        user.password_hash = hash_password(new_pw)
        await user.save()

        # Revoke other sessions on password change
        sessions = await Session.find(
            Session.user_id == str(user.id),
            Session.revoked == False,
        ).to_list()
        for s in sessions:
            s.revoked = True
            await s.save()

        await write_audit(
            organization_id=user.organization_id,
            actor_id=str(user.id),
            action="user.changed_password",
            resource_type="user",
            resource_id=str(user.id),
        )

    @staticmethod
    async def list_sessions(user: User) -> list[dict]:
        now = utcnow()
        sessions = await Session.find(
            Session.user_id == str(user.id),
            Session.revoked == False,
            Session.expires_at > now,
        ).to_list()

        return [
            {
                "id": str(s.id),
                "user_agent": s.user_agent,
                "created_at": s.created_at,
                "expires_at": s.expires_at,
            }
            for s in sessions
        ]

    @staticmethod
    async def revoke_session(user: User, session_id: str) -> None:
        session = await Session.get(session_id)
        if not session or session.user_id != str(user.id):
            raise AppError("NOT_FOUND", "Session not found", 404)
        session.revoked = True
        await session.save()

    @staticmethod
    async def export_data(user: User) -> dict:
        # GDPR compliance data export
        invoices = await Invoice.find(
            Invoice.uploaded_by == str(user.id),
            Invoice.is_deleted == False,
        ).to_list()
        audits = await AuditLog.find(
            AuditLog.actor_id == str(user.id),
        ).to_list()

        return {
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value,
                "department": user.department,
                "created_at": user.created_at.isoformat(),
            },
            "uploaded_invoices": [
                {
                    "id": str(i.id),
                    "filename": i.original_filename,
                    "vendor_name": i.vendor_name,
                    "total": i.total,
                    "status": i.status.value,
                    "created_at": i.created_at.isoformat(),
                }
                for i in invoices
            ],
            "audit_actions": [
                {
                    "action": a.action,
                    "resource_type": a.resource_type,
                    "resource_id": a.resource_id,
                    "created_at": a.created_at.isoformat(),
                }
                for a in audits
            ],
        }

    @staticmethod
    async def delete_account(user: User, confirm_text: str) -> None:
        if confirm_text != "DELETE":
            raise AppError("CONFIRM_TEXT_MISMATCH", "Confirmation text must be 'DELETE'", 400)

        # If user is admin, check if they are the only active admin
        if user.role == UserRole.admin:
            active_admins = await User.find(
                User.organization_id == user.organization_id,
                User.role == UserRole.admin,
                User.is_deleted == False,
            ).count()
            if active_admins <= 1:
                raise AppError(
                    "CANNOT_SELF_DEMOTE",
                    "Cannot delete the only admin account in the organization",
                    400,
                )

        user.is_deleted = True
        await user.save()

        # Revoke all sessions
        sessions = await Session.find(Session.user_id == str(user.id)).to_list()
        for s in sessions:
            s.revoked = True
            await s.save()

    @staticmethod
    async def list_org_users(org_id: str) -> list[User]:
        return await User.find(
            User.organization_id == org_id,
            User.is_deleted == False,
        ).to_list()

    @staticmethod
    async def create_user(
        actor: User,
        email: str,
        password: str,
        full_name: str,
        role: UserRole,
        department: str,
    ) -> User:
        normalized_email = email.strip().lower()
        existing = await User.find_one(User.email == normalized_email)
        if existing:
            raise AppError("CONFLICT", "Email address is already registered", 409)

        new_user = User(
            organization_id=actor.organization_id,
            email=normalized_email,
            password_hash=hash_password(password),
            full_name=full_name.strip(),
            role=role,
            department=department.strip(),
        )
        await new_user.insert()

        await write_audit(
            organization_id=actor.organization_id,
            actor_id=str(actor.id),
            action="user.created",
            resource_type="user",
            resource_id=str(new_user.id),
            after={"email": normalized_email, "role": role.value},
        )
        return new_user

    @staticmethod
    async def update_user_role(actor: User, target_user_id: str, new_role: UserRole) -> User:
        target = await User.get(target_user_id)
        if not target or target.is_deleted or str(target.organization_id) != str(actor.organization_id):
            raise AppError("NOT_FOUND", "User not found", 404)

        if str(actor.id) == str(target.id) and new_role != UserRole.admin:
            # Check if this admin is the last one
            admin_count = await User.find(
                User.organization_id == actor.organization_id,
                User.role == UserRole.admin,
                User.is_deleted == False,
            ).count()
            if admin_count <= 1:
                raise AppError("CANNOT_SELF_DEMOTE", "Cannot remove the only admin in the organization", 403)

        before_role = target.role.value
        target.role = new_role
        await target.save()

        await write_audit(
            organization_id=actor.organization_id,
            actor_id=str(actor.id),
            action="user.role_changed",
            resource_type="user",
            resource_id=str(target.id),
            before={"role": before_role},
            after={"role": new_role.value},
        )
        return target
