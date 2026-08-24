---
name: finguard-backend-runner
description: Runs, tests, and manages the FinGuard FastAPI backend server, verifies MongoDB Atlas connectivity, and executes API test workflows using Postman collection endpoints.
---

# FinGuard Backend Runner & API Testing Guide

This skill provides step-by-step instructions and automated runner scripts to start, verify, and test the FinGuard FastAPI backend.

---

## 1. Starting the Backend Server

Always run the backend inside `backend/` using the dedicated virtual environment `.venv`:

```powershell
cd backend
.venv\Scripts\uvicorn app.main:app --reload --port 5000
```

### Health Verification Endpoints:
- **Liveness**: `GET http://localhost:5000/health` (Returns `200 OK`)
- **Readiness (MongoDB Ping)**: `GET http://localhost:5000/ready` (Returns `200 OK`, `{"status": "ready", "database": "connected"}`)
- **Swagger Interactive Docs**: `http://localhost:5000/docs`
- **ReDoc Interactive Docs**: `http://localhost:5000/redoc`

---

## 2. Running Automated Tests

Run the full Pytest test suite:

```powershell
cd backend
.venv\Scripts\pytest tests/ -v
```

Linting check with Ruff:
```powershell
cd backend
.venv\Scripts\ruff check app/ tests/
```

---

## 3. Postman Collection & Testing

The master Postman collection and environment templates live at:
- **Collection**: [`backend/postman/collection.json`](file:///c:/Users/Lenovo/Desktop/Finguard/backend/postman/collection.json)
- **Environment**: [`backend/postman/environment.json`](file:///c:/Users/Lenovo/Desktop/Finguard/backend/postman/environment.json)

### Core Request Workflow:
1. **Register Admin**: `POST /api/v1/auth/register` with `email`, `password`, `full_name`, `organization_name`.
2. **Login**: `POST /api/v1/auth/login` with `email`, `password` (captures `accessToken` & `refresh_token` cookie).
3. **Upload Invoice**: `POST /api/v1/invoices` (multipart upload up to 50 files).
4. **View Exceptions**: `GET /api/v1/exceptions?status=open`.
5. **Decide Approval**: `POST /api/v1/approvals/{id}/decide` with `{"decision": "approve"}`.
6. **Fetch Dashboard Stats**: `GET /api/v1/reports/dashboard-stats`.

---

## 4. One-Click Smoke Test Script

To run an automated end-to-end smoke test against the live backend:

```powershell
cd backend
.venv\Scripts\python ../.agents/skills/finguard-backend-runner/scripts/api_runner.py
```
