from datetime import UTC, datetime, timedelta

import jwt

from app.config.env import settings
from app.core.errors import AppError


def _parse_duration(value: str) -> timedelta:
    unit = value[-1]
    amount = int(value[:-1])
    if unit == "m":
        return timedelta(minutes=amount)
    if unit == "h":
        return timedelta(hours=amount)
    if unit == "d":
        return timedelta(days=amount)
    raise ValueError(f"Unsupported duration: {value}")


def sign_access(user_id: str, organization_id: str, role: str) -> str:
    exp = datetime.now(UTC) + _parse_duration(settings.jwt_access_expires_in)
    return jwt.encode(
        {
            "sub": user_id,
            "org": organization_id,
            "role": role,
            "typ": "access",
            "exp": exp,
        },
        settings.jwt_access_secret,
        algorithm="HS256",
    )


def sign_email_action(approval_id: str, action: str) -> str:
    exp = datetime.now(UTC) + timedelta(days=2)
    return jwt.encode(
        {"sub": approval_id, "act": action, "typ": "email_action", "exp": exp},
        settings.jwt_access_secret,
        algorithm="HS256",
    )


def verify_email_action(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_access_secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as exc:
        raise AppError("TOKEN_EXPIRED", "Action link expired", 401) from exc
    except jwt.InvalidTokenError as exc:
        raise AppError("TOKEN_INVALID", "Invalid action token", 401) from exc
    if payload.get("typ") != "email_action":
        raise AppError("TOKEN_INVALID", "Invalid action token", 401)
    return payload


def decode_access(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_access_secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as exc:
        raise AppError("TOKEN_EXPIRED", "Access token expired", 401) from exc
    except jwt.InvalidTokenError as exc:
        raise AppError("TOKEN_INVALID", "Token tampered or invalid", 401) from exc
    if payload.get("typ") != "access":
        raise AppError("TOKEN_INVALID", "Token tampered or invalid", 401)
    return payload
