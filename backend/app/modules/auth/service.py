import re
import secrets
from datetime import timedelta

from app.core.errors import AppError
from app.core.security import hash_password, verify_password
from app.models.documents import Organization, Session, User, UserRole
from app.modules.invoices.service import seed_org_defaults
from app.utils.datetime import utcnow
from app.utils.jwt import sign_access


def _generate_slug(name: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower()).strip("-")
    return f"{cleaned}-{secrets.token_hex(3)}"


class AuthService:
    @staticmethod
    async def register(
        email: str,
        password: str,
        full_name: str,
        organization_name: str,
        user_agent: str = "",
    ) -> tuple[dict, str]:
        normalized_email = email.strip().lower()
        existing = await User.find_one(User.email == normalized_email)
        if existing:
            raise AppError("EMAIL_ALREADY_REGISTERED", "Email address is already registered", 409)

        org = Organization(
            name=organization_name.strip(),
            slug=_generate_slug(organization_name),
            approval_threshold=1000.0,
        )
        await org.insert()
        org_id = str(org.id)

        await seed_org_defaults(org_id)

        user = User(
            organization_id=org_id,
            email=normalized_email,
            password_hash=hash_password(password),
            full_name=full_name.strip(),
            role=UserRole.admin,
            department="Executive",
        )
        await user.insert()
        user_id = str(user.id)
        secret = secrets.token_hex(32)
        expires_at = utcnow() + timedelta(days=7)
        session = Session(
            user_id=user_id,
            organization_id=org_id,
            refresh_hash=hash_password(secret),
            user_agent=user_agent,
            expires_at=expires_at,
        )
        await session.insert()
        session_id = str(session.id)
        refresh_cookie = f"{session_id}.{secret}"

        access_token = sign_access(user_id, org_id, user.role.value)
        data = {
            "access_token": access_token,
            "token_type": "Bearer",
            "user": {
                "id": user_id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value,
                "department": user.department,
                "organization_id": org_id,
            },
        }
        return data, refresh_cookie

    @staticmethod
    async def login(
        email: str,
        password: str,
        user_agent: str = "",
    ) -> tuple[dict, str]:
        normalized_email = email.strip().lower()
        user = await User.find_one(User.email == normalized_email, User.is_deleted == False)
        if not user or not user.password_hash:
            raise AppError("UNAUTHORIZED", "Invalid email or password", 401)

        now = utcnow()
        if user.locked_until and user.locked_until > now:
            minutes_left = int((user.locked_until - now).total_seconds() / 60) + 1
            raise AppError(
                "FORBIDDEN",
                f"Account locked due to 5 failed login attempts. Try again in {minutes_left} minutes.",
                423,
            )

        if not verify_password(password, user.password_hash):
            user.failed_login_count += 1
            if user.failed_login_count >= 5:
                user.locked_until = now + timedelta(minutes=15)
                await user.save()
                raise AppError(
                    "FORBIDDEN", "Account locked due to 5 failed login attempts. Try again in 15 minutes.", 423
                )
            await user.save()
            raise AppError("UNAUTHORIZED", "Invalid email or password", 401)

        # Reset failed count on successful login
        user.failed_login_count = 0
        user.locked_until = None
        await user.save()

        secret = secrets.token_hex(32)
        expires_at = now + timedelta(days=7)
        session = Session(
            user_id=str(user.id),
            organization_id=str(user.organization_id),
            refresh_hash=hash_password(secret),
            user_agent=user_agent,
            expires_at=expires_at,
        )
        await session.insert()
        refresh_cookie = f"{session.id}.{secret}"

        access_token = sign_access(str(user.id), str(user.organization_id), user.role.value)
        data = {
            "access_token": access_token,
            "token_type": "Bearer",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value,
                "department": user.department,
                "organization_id": str(user.organization_id),
            },
        }
        return data, refresh_cookie

    @staticmethod
    async def refresh(cookie_val: str, user_agent: str = "") -> tuple[dict, str]:
        if not cookie_val or "." not in cookie_val:
            raise AppError("REFRESH_TOKEN_INVALID", "Invalid refresh token", 401)

        parts = cookie_val.split(".", 1)
        session_id, secret = parts[0], parts[1]

        session = await Session.get(session_id)
        now = utcnow()

        if not session or session.revoked or session.expires_at < now:
            if session and session.revoked:
                # Reuse of rotated refresh token -> breach signal! Revoke all sessions for user
                all_sessions = await Session.find(Session.user_id == session.user_id).to_list()
                for s in all_sessions:
                    s.revoked = True
                    await s.save()
            raise AppError("REFRESH_TOKEN_INVALID", "Refresh token expired or already used", 401)

        if not verify_password(secret, session.refresh_hash):
            raise AppError("REFRESH_TOKEN_INVALID", "Invalid refresh token secret", 401)

        # Invalidate old session (token rotation)
        session.revoked = True
        await session.save()

        user = await User.get(session.user_id)
        if not user or user.is_deleted:
            raise AppError("UNAUTHORIZED", "User no longer active", 401)

        # Issue new rotated session
        new_secret = secrets.token_hex(32)
        new_expires_at = now + timedelta(days=7)
        new_session = Session(
            user_id=str(user.id),
            organization_id=str(user.organization_id),
            refresh_hash=hash_password(new_secret),
            user_agent=user_agent,
            expires_at=new_expires_at,
        )
        await new_session.insert()
        new_cookie = f"{new_session.id}.{new_secret}"

        access_token = sign_access(str(user.id), str(user.organization_id), user.role.value)
        data = {
            "access_token": access_token,
            "token_type": "Bearer",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value,
                "department": user.department,
                "organization_id": str(user.organization_id),
            },
        }
        return data, new_cookie

    @staticmethod
    async def logout(cookie_val: str | None) -> None:
        if cookie_val and "." in cookie_val:
            session_id = cookie_val.split(".", 1)[0]
            session = await Session.get(session_id)
            if session:
                session.revoked = True
                await session.save()

    @staticmethod
    async def google_login(code: str, user_agent: str = "") -> tuple[dict, str]:
        from app.config.env import settings
        if not settings.google_client_id or not settings.google_client_secret:
            raise AppError("INVALID_REQUEST", "Google OAuth is not configured", 400)

        # Exchange authorization code for tokens
        import httpx
        async with httpx.AsyncClient(timeout=10.0) as client:
            token_res = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "redirect_uri": settings.google_callback_url,
                    "grant_type": "authorization_code",
                },
            )
            if token_res.status_code != 200:
                raise AppError("UNAUTHORIZED", "Failed to exchange Google authorization code", 401)
            
            google_tokens = token_res.json()
            id_token_val = google_tokens.get("id_token")
            google_access = google_tokens.get("access_token")

            # Fetch user info
            userinfo_res = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {google_access}"},
            )
            if userinfo_res.status_code != 200:
                raise AppError("UNAUTHORIZED", "Failed to fetch Google user profile", 401)
            
            profile = userinfo_res.json()
            email = profile.get("email", "").strip().lower()
            google_sub = profile.get("sub", "")
            full_name = profile.get("name", "Google User")

        if not email:
            raise AppError("BAD_REQUEST", "Google account email is missing", 400)

        # Find or create user
        user = await User.find_one(User.email == email)
        if user:
            if not user.google_sub:
                user.google_sub = google_sub
                await user.save()
        else:
            # Create organization and user
            org_name = f"{full_name}'s Organization"
            org = Organization(
                name=org_name,
                slug=_generate_slug(org_name),
                approval_threshold=1000.0,
            )
            await org.insert()
            org_id = str(org.id)
            await seed_org_defaults(org_id)

            user = User(
                organization_id=org_id,
                email=email,
                google_sub=google_sub,
                full_name=full_name,
                role=UserRole.admin,
                department="Executive",
            )
            await user.insert()

        # Issue session & tokens
        now = utcnow()
        secret = secrets.token_hex(32)
        expires_at = now + timedelta(days=7)
        session = Session(
            user_id=str(user.id),
            organization_id=str(user.organization_id),
            refresh_hash=hash_password(secret),
            user_agent=user_agent,
            expires_at=expires_at,
        )
        await session.insert()
        refresh_cookie = f"{session.id}.{secret}"

        access_token = sign_access(str(user.id), str(user.organization_id), user.role.value)
        data = {
            "access_token": access_token,
            "token_type": "Bearer",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value,
                "department": user.department,
                "organization_id": str(user.organization_id),
            },
        }
        return data, refresh_cookie
