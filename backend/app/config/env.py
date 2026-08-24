from __future__ import annotations

import sys

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    port: int = 5000
    mongodb_uri: str
    mongodb_db: str = "finguard"
    jwt_access_secret: str
    jwt_refresh_secret: str
    jwt_access_expires_in: str = "15m"
    jwt_refresh_expires_in: str = "7d"
    client_url: str = "http://localhost:5173"
    cors_origins: str = "http://localhost:5173"
    cookie_secure: bool = False
    encryption_key: str
    upload_dir: str = "./uploads"
    max_upload_bytes: int = 25 * 1024 * 1024
    extraction_provider: str = "mock"
    extraction_http_url: str = ""
    queue_backend: str = "inline"
    redis_url: str = "redis://localhost:6379/0"
    confidence_threshold: float = 0.85
    google_client_id: str = ""
    google_client_secret: str = ""
    google_callback_url: str = "http://localhost:5000/api/v1/auth/google/callback"
    smtp_host: str = ""
    smtp_port: int = 465
    smtp_user: str = ""
    smtp_pass: str = ""
    email_from: str = "noreply@finguard.local"
    sentry_dsn: str = ""

    @field_validator("jwt_access_secret", "jwt_refresh_secret")
    @classmethod
    def _secrets_min_len(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError("JWT secrets must be at least 32 characters")
        return v

    @field_validator("encryption_key")
    @classmethod
    def _enc_key(cls, v: str) -> str:
        if len(v) != 64:
            raise ValueError("ENCRYPTION_KEY must be 64 hex characters (32 bytes)")
        bytes.fromhex(v)
        return v


def load_settings() -> Settings:
    try:
        settings = Settings()  # type: ignore[call-arg]
    except Exception as exc:
        print(f"Invalid environment variables: {exc}", file=sys.stderr)
        sys.exit(1)
    if settings.jwt_access_secret == settings.jwt_refresh_secret:
        print("JWT_ACCESS_SECRET and JWT_REFRESH_SECRET must differ", file=sys.stderr)
        sys.exit(1)
    return settings


settings = load_settings()
