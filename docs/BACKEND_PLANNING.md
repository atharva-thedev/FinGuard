# FinGuard Backend Planning

Companion to [`Finguard_prd.md`](../Finguard_prd.md). Maps product MVP stages onto a FastAPI API that follows [`instruction.md`](../instruction.md) practices (envelope, auth, tenancy, security, CI) without copying the Express stack.

**Status:** Phase 1 MVP backend (no frontend).  
**Verified at scaffold (2026-08-23):** FastAPI **0.141.1** on PyPI. Other pins live in [`backend/pyproject.toml`](../backend/pyproject.toml) as `>=` ranges — re-check PyPI before bumps. Do not copy versions from the PRD table.

---

## 1. Principles from instruction.md (adapted)

| Practice | How FinGuard implements it |
| --- | --- |
| Crash on bad env | Pydantic Settings in `app/config/env.py` — process exits if required vars fail |
| `/api/v1` versioning | All business routes under this prefix |
| Success/error envelope | `{ success: true, data }` and `{ success: false, error: { code, message, fields? } }` |
| JWT 15m + refresh 7d HttpOnly | Access in JSON; refresh cookie `HttpOnly; Secure; SameSite=Strict`; rotation; reuse = revoke all sessions |
| Ownership | **Org-scoped** `assert_org_access` (not user-only). 404 if other org; 403 if same org, wrong role |
| Soft delete | `is_deleted` + `deleted_at` on tenant resources |
| Rate limits | Global `/api`; stricter `/api/v1/auth`; `/health` and `/ready` excluded |
| JSON vs uploads | JSON bodies capped (~32 KB). Multipart invoice upload is a separate route (25 MB) |
| Health | `GET /health` liveness; `GET /ready` Mongo ping |
| Audit | Immutable `audit_logs` on state changes |
| Secrets | Never in git; `.env.example` only |
| Jobs | `QUEUE_BACKEND=inline` (default, no Redis) or `celery` when Redis is configured |

---

## 2. Module map

```
backend/app/
  main.py                 # FastAPI factory
  config/env.py, db.py
  core/errors.py, security.py
  middleware/
  utils/jwt, encryption, ownership, token_compare
  models/documents.py     # Beanie documents (init list)
  realtime/hub.py         # org-scoped WebSocket rooms
  modules/
    auth/                 # register, login, refresh, logout, Google (if env set)
    users/                # me, sessions, export, admin user list
    organizations/        # org settings
    invoices/             # upload, list, get, patch extraction
    extraction/           # provider interface + mock
    vendors/
    categories/
    policies/             # budget + hard rules
    approvals/
    exceptions/           # unified queue
    audit/
    reports/
    notifications/        # email stub (SMTP optional)
  workers/extraction.py   # inline or Celery
```

---

## 3. Tenant ownership

Every tenant collection includes `organization_id`.

```
assert_org_access(doc, current_user.organization_id)
  -> missing or other org: 404 NOT_FOUND (do not leak existence)
role_guard(allowed_roles)
  -> wrong role, same org: 403 FORBIDDEN
```

List queries always filter `{ organization_id, is_deleted: false }`.

---

## 4. Invoice status machine

`captured` → `extracting` → `needs_review` | `validated` → `pending_approval` | `exception` → `approved` | `rejected`

Low-confidence fields (< 85%) force `needs_review`. Exact duplicates force `exception` (block). Fuzzy duplicates warn but do not auto-block.

---

## 5. Extraction providers

`EXTRACTION_PROVIDER=mock|http`

- **mock** (default): deterministic fields for tests; filenames containing `lowconf` get < 85% confidence.
- **http**: POST file to `EXTRACTION_HTTP_URL` (adapter for Textract/Document AI/LLM later). Never auto-accept low-confidence fields.

---

## 6. Error codes

Same set as instruction.md: `VALIDATION_ERROR`, `INVALID_REQUEST`, `UNAUTHORIZED`, `TOKEN_EXPIRED`, `TOKEN_INVALID`, `REFRESH_TOKEN_INVALID`, `FORBIDDEN`, `NOT_FOUND`, `CONFLICT`, `RATE_LIMIT_EXCEEDED`, `INTERNAL_ERROR`.

---

## 7. Auth cookie

- Name: `refresh_token`
- Value: `{session_id}.{secret}`
- Path: `/api/v1/auth`
- Secret stored bcrypt-hashed on `sessions`; lookup by `session_id`

---

## 8. Roles (PRD §12)

| Role | Typical API access |
| --- | --- |
| `admin` | Users, org, policies, all invoices |
| `controller` | Policies, exceptions, reports, invoices |
| `approver` | Own approval inbox |
| `ap_clerk` | Upload, extraction overrides, duplicate exceptions |
| `viewer` | Read-only invoices, reports, audit |

---

## 9. Runbook

See [`backend/README.md`](../backend/README.md).
