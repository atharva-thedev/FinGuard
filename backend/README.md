# FinGuard backend

FastAPI + MongoDB API for invoice capture, extraction review, policy checks, and approvals.

## Setup

1. Copy `.env.example` to `.env` and replace JWT secrets and `ENCRYPTION_KEY` (64 hex chars).
2. Run MongoDB locally or set `MONGODB_URI` to Atlas.
3. Install and run:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

`QUEUE_BACKEND=inline` processes OCR jobs in-process (no Redis). Set `QUEUE_BACKEND=celery` and start a worker when you need a queue:

```bash
celery -A app.workers.celery_app.celery worker --loglevel=info
```

## First requests

1. `POST /api/v1/auth/register` — `{ "email", "password", "full_name", "organization_name" }`
2. `POST /api/v1/auth/login` — sets refresh cookie, returns `accessToken`
3. `POST /api/v1/invoices` — multipart `files`

See `../docs/BACKEND_PLANNING.md` and `postman/`.
