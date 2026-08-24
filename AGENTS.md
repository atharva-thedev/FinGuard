# FinGuard Engineering & Documentation Rules

## 1. Continuous API Documentation & Postman Synchronization (Mandatory)
Whenever any backend route (`app/modules/**/router.py`), schema (`schemas.py`), model (`documents.py`), or error response format is added or modified:
1. **Update [`docs/API_DOCUMENTATION.md`](docs/API_DOCUMENTATION.md)** immediately to reflect the new parameters, request/response models, status codes, and error codes.
2. **Update [`backend/postman/collection.json`](backend/postman/collection.json)** to include the new/updated endpoint definitions.
3. **Verify** with `cd backend && .venv\Scripts\pytest tests/ -v` and `api_runner.py`.

## 2. Security & Tenancy Rules
- Multi-tenancy must be enforced on every query with `organization_id`.
- Cross-tenant access must return `404 NOT_FOUND` via `assert_org_access` (never `403`) to prevent existence leakage.
- Passwords must use `bcrypt` (12 rounds) and sensitive ERP tokens must use `AES-256-GCM`.
