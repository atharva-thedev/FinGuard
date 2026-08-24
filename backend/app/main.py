from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.config.db import connect_db, disconnect_db, ping_db
from app.config.env import settings
from app.middleware.error_handler import register_error_handlers
from app.middleware.security_headers import SecurityHeadersMiddleware

# Import modular routers
from app.modules.approvals.router import router as approvals_router
from app.modules.audit.router import router as audit_router
from app.modules.auth.router import router as auth_router
from app.modules.categories.router import router as categories_router
from app.modules.exceptions.router import router as exceptions_router
from app.modules.invoices.router import router as invoices_router
from app.modules.organizations.router import router as orgs_router
from app.modules.policies.router import router as policies_router
from app.modules.reports.router import router as reports_router
from app.modules.users.router import router as users_router
from app.modules.vendors.router import router as vendors_router
from app.realtime.router import router as realtime_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_db()
    yield
    # Shutdown
    await disconnect_db()


# Initialize SlowAPI rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI(
    title="FinGuard API",
    description="AI-powered invoice and expense management backend API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Attach limiter state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 1. Security headers (Helmet equivalent)
app.add_middleware(SecurityHeadersMiddleware)

# 2. CORS configuration with explicit origin allowlist
origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or [settings.client_url],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# 3. Global central error handlers
register_error_handlers(app)


# 4. Health & Readiness endpoints (unauthenticated)
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "finguard-backend", "env": settings.app_env}


@app.get("/ready", tags=["Health"])
async def readiness_check():
    db_ok = await ping_db()
    if not db_ok:
        return JSONResponse(
            status_code=503,
            content={"status": "unavailable", "database": "disconnected"},
        )
    return {"status": "ready", "database": "connected"}


# 5. Assemble API v1 Routers
api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(auth_router)
api_v1.include_router(users_router)
api_v1.include_router(orgs_router)
api_v1.include_router(invoices_router)
api_v1.include_router(vendors_router)
api_v1.include_router(categories_router)
api_v1.include_router(policies_router)
api_v1.include_router(approvals_router)
api_v1.include_router(exceptions_router)
api_v1.include_router(audit_router)
api_v1.include_router(reports_router)
api_v1.include_router(realtime_router)

app.include_router(api_v1)
