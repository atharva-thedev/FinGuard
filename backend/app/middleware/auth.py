from datetime import UTC, datetime

from fastapi import Depends, Header

from app.core.errors import AppError
from app.models.documents import User
from app.utils.jwt import decode_access


from app.utils.datetime import utcnow


async def get_current_user(
    authorization: str | None = Header(None, alias="Authorization"),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise AppError("UNAUTHORIZED", "Authentication required", 401)

    token = authorization[7:].strip()
    if not token:
        raise AppError("UNAUTHORIZED", "Authentication required", 401)

    payload = decode_access(token)
    user_id = payload.get("sub")
    org_id = payload.get("org")

    if not user_id or not org_id:
        raise AppError("TOKEN_INVALID", "Invalid token claims", 401)

    user = await User.get(user_id)
    if not user or user.is_deleted or str(user.organization_id) != str(org_id):
        raise AppError("UNAUTHORIZED", "User not found or deactivated", 401)

    if user.locked_until and user.locked_until > utcnow():
        raise AppError("FORBIDDEN", "Account is temporarily locked due to multiple failed login attempts", 403)

    return user


async def require_auth(user: User = Depends(get_current_user)) -> User:
    return user
