---
description: Mandatory rule to automatically synchronize and update API_DOCUMENTATION.md and postman collection whenever API routes, models, schemas, or error handlers are modified.
globs: ["backend/app/modules/**", "backend/app/models/**", "backend/app/main.py", "backend/app/middleware/**"]
---

# Rule: Continuous API Documentation & Postman Synchronization

Whenever you add, modify, deprecate, or refactor any backend endpoint, schema, model, or error handler in the `backend/app/` directory, you **MUST** immediately update the API documentation and testing artifacts as part of the same task.

---

## 1. Trigger Files
This rule triggers whenever changes are made to:
- `backend/app/modules/**/router.py` (Endpoints, routes, HTTP methods)
- `backend/app/modules/**/schemas.py` (Request/response payloads, field validations)
- `backend/app/models/documents.py` (Database models, enums, status transitions)
- `backend/app/middleware/error_handler.py` or error codes (Error format, codes, status codes)
- `backend/app/main.py` (Mounted routers, lifespan events, middleware stack)

---

## 2. Mandatory Synchronization Actions

### A. Update `docs/API_DOCUMENTATION.md`
1. **Endpoint Specs**: Add or update the endpoint's HTTP method, path, authentication requirement, RBAC role guard, request body schema, and all possible HTTP status codes (`200`, `201`, `400`, `401`, `403`, `404`, `409`, `422`, `423`, `429`, `500`).
2. **Lifecycle Scenarios**: If the change introduces or modifies an invoice/approval state transition, update the Mermaid diagram and scenario walkthroughs in Section 4.
3. **Error Catalog**: If any new machine-readable error code is introduced, add it to Section 6 with trigger conditions and developer remediation steps.

### B. Update `backend/postman/collection.json`
1. Add new request items under the appropriate module folder (`System`, `Auth`, `Users`, `Invoices`, `Vendors`, `Categories`, `Policies`, `Approvals`, `Exceptions`, `Reports`).
2. Ensure URLs use `{{baseUrl}}` and headers include `Authorization: Bearer {{accessToken}}` where required.
3. Include realistic raw JSON bodies in request definitions.

### C. Run Verification
1. Execute pytest suite: `cd backend && .venv\Scripts\pytest tests/ -v`
2. Execute automated smoke test: `cd backend && .venv\Scripts\python ../.agents/skills/finguard-backend-runner/scripts/api_runner.py`
