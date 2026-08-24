from fastapi import APIRouter, Depends

from app.core.responses import ok
from app.middleware.auth import require_auth
from app.middleware.role_guard import require_roles
from app.models.documents import User, UserRole
from app.modules.users.schemas import (
    ChangePasswordRequest,
    CreateUserRequest,
    DeleteAccountRequest,
    UpdateProfileRequest,
    UpdateUserRoleRequest,
)
from app.modules.users.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def _format_user(u: User) -> dict:
    return {
        "id": str(u.id),
        "email": u.email,
        "full_name": u.full_name,
        "role": u.role.value,
        "department": u.department,
        "organization_id": str(u.organization_id),
        "created_at": u.created_at,
    }


@router.get("/me")
async def get_me(user: User = Depends(require_auth)):
    return ok(_format_user(user))


@router.patch("/me")
async def update_me(
    payload: UpdateProfileRequest,
    user: User = Depends(require_auth),
):
    updated = await UserService.update_profile(user, payload.full_name, payload.department)
    return ok(_format_user(updated))


@router.post("/me/change-password")
async def change_password(
    payload: ChangePasswordRequest,
    user: User = Depends(require_auth),
):
    await UserService.change_password(user, payload.current_password, payload.new_password)
    return ok({"message": "Password changed successfully"})


@router.get("/me/sessions")
async def list_sessions(user: User = Depends(require_auth)):
    sessions = await UserService.list_sessions(user)
    return ok(sessions)


@router.delete("/me/sessions/{session_id}")
async def revoke_session(
    session_id: str,
    user: User = Depends(require_auth),
):
    await UserService.revoke_session(user, session_id)
    return ok({"message": "Session revoked"})


@router.get("/me/export")
async def export_my_data(user: User = Depends(require_auth)):
    data = await UserService.export_data(user)
    return ok(data)


@router.delete("/me")
async def delete_my_account(
    payload: DeleteAccountRequest,
    user: User = Depends(require_auth),
):
    await UserService.delete_account(user, payload.confirm_text)
    return ok({"message": "Account deleted"})


@router.get("", dependencies=[Depends(require_roles(UserRole.admin, UserRole.controller))])
async def list_users(user: User = Depends(require_auth)):
    users = await UserService.list_org_users(str(user.organization_id))
    return ok([_format_user(u) for u in users])


@router.post("", status_code=201, dependencies=[Depends(require_roles(UserRole.admin))])
async def create_user(
    payload: CreateUserRequest,
    user: User = Depends(require_auth),
):
    new_user = await UserService.create_user(
        actor=user,
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
        role=payload.role,
        department=payload.department,
    )
    return ok(_format_user(new_user), status_code=201)


@router.patch("/{user_id}/role", dependencies=[Depends(require_roles(UserRole.admin))])
async def update_user_role(
    user_id: str,
    payload: UpdateUserRoleRequest,
    user: User = Depends(require_auth),
):
    updated = await UserService.update_user_role(user, user_id, payload.role)
    return ok(_format_user(updated))
