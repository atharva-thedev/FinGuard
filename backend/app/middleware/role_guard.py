from collections.abc import Callable

from fastapi import Depends

from app.core.errors import AppError
from app.middleware.auth import require_auth
from app.models.documents import User, UserRole


def require_roles(*allowed_roles: UserRole | str) -> Callable:
    allowed_values = {r.value if isinstance(r, UserRole) else str(r) for r in allowed_roles}

    async def _role_checker(user: User = Depends(require_auth)) -> User:
        user_role = user.role.value if isinstance(user.role, UserRole) else str(user.role)
        if user_role not in allowed_values:
            raise AppError("FORBIDDEN", "Insufficient permissions for this action", 403)
        return user

    return _role_checker
