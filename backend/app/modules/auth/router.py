from fastapi import APIRouter, Cookie, Header, Request, Response

from app.config.env import settings
from app.core.responses import ok
from app.modules.auth.schemas import LoginRequest, RegisterRequest
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


def _set_refresh_cookie(response: Response, cookie_val: str) -> None:
    response.set_cookie(
        key="refresh_token",
        value=cookie_val,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="strict",
        path="/api/v1/auth",
        max_age=7 * 24 * 3600,
    )


def _clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(
        key="refresh_token",
        path="/api/v1/auth",
        httponly=True,
        secure=settings.cookie_secure,
        samesite="strict",
    )


@router.post("/register", status_code=201)
async def register(
    payload: RegisterRequest,
    request: Request,
    user_agent: str | None = Header(None, alias="User-Agent"),
):
    data, refresh_cookie = await AuthService.register(
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
        organization_name=payload.organization_name,
        user_agent=user_agent or "",
    )
    res = ok(data, status_code=201)
    _set_refresh_cookie(res, refresh_cookie)
    return res


@router.post("/login")
async def login(
    payload: LoginRequest,
    request: Request,
    user_agent: str | None = Header(None, alias="User-Agent"),
):
    data, refresh_cookie = await AuthService.login(
        email=payload.email,
        password=payload.password,
        user_agent=user_agent or "",
    )
    res = ok(data)
    _set_refresh_cookie(res, refresh_cookie)
    return res


@router.post("/refresh")
async def refresh(
    request: Request,
    refresh_token: str | None = Cookie(None, alias="refresh_token"),
    user_agent: str | None = Header(None, alias="User-Agent"),
):
    data, new_cookie = await AuthService.refresh(
        cookie_val=refresh_token or "",
        user_agent=user_agent or "",
    )
    res = ok(data)
    _set_refresh_cookie(res, new_cookie)
    return res


@router.post("/logout")
async def logout(
    refresh_token: str | None = Cookie(None, alias="refresh_token"),
):
    await AuthService.logout(refresh_token)
    res = ok({"logged_out": True})
    _clear_refresh_cookie(res)
    return res


@router.get("/google")
async def google_auth():
    # If Google OAuth credentials configured, provide redirect URL
    if not settings.google_client_id:
        from app.core.errors import AppError
        raise AppError("INVALID_REQUEST", "Google OAuth is not configured", 400)
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={settings.google_client_id}&"
        f"redirect_uri={settings.google_callback_url}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile&"
        f"access_type=offline"
    )
    return ok({"auth_url": auth_url})


@router.get("/google/callback")
async def google_callback(
    code: str,
    user_agent: str | None = Header(None, alias="User-Agent"),
):
    data, refresh_cookie = await AuthService.google_login(code, user_agent=user_agent or "")
    res = ok(data)
    _set_refresh_cookie(res, refresh_cookie)
    return res
