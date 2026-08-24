# FinGuard — Product Requirements Document (PRD)

### v1.0 — Complete Draft

> **Note on assumptions:** Where prior discussion didn't specify an answer, this draft makes a reasonable, stated assumption marked `[Assumption]` so the document is complete and usable rather than a shell. Review and override any assumption before treating this as final.

---

## 0. Document Control


| Field          | Value                              |
| -------------- | ---------------------------------- |
| Product name   | FinGuard                           |
| Tagline        | Protect • Analyze • Optimize       |
| Document owner | *[fill in]*                        |
| Version        | 1.1 (backend-aligned)              |
| Last updated   | 2026-08-23                         |
| Status         | Draft — backend MVP in progress    |


---

## 1. Executive Summary

FinGuard is an **AI-powered invoice and expense management platform** that automates the full lifecycle of a business expense — from capture through payment — while continuously protecting the organization from fraud, policy violations, and budget overruns. It combines OCR/AI data extraction, 3-way matching, AI risk scoring, and a natural-language "Finance Copilot" into a single system of record, positioned as an **enterprise SaaS + AI finance intelligence** product rather than a simple invoicing tool.

**One-line pitch:** *FinGuard turns invoice and expense processing from a manual bottleneck into an automated, AI-monitored control system.*

`[Assumption]` Target customer: mid-market companies (100–2,000 employees) with an existing AP function and at least one ERP/accounting system, who process >500 invoices/month — enough volume that manual review is genuinely painful and AI extraction has enough data to be useful, but small enough to not require SAP-scale integration work in v1.

---

## 2. Problem Statement

Mid-market finance teams process invoices largely manually: PDFs/emails land in an inbox, an AP clerk keys line items into an ERP by hand, matches them against POs on a spreadsheet, and routes approvals over email or Slack. This creates:

- **Time cost:** `[Assumption]` 10–15 minutes of manual handling per invoice at typical volume, meaning a mid-size AP team spends the equivalent of 1–2 full-time roles just on data entry and matching.
- **Error and fraud exposure:** duplicate payments, missed price mismatches, and fabricated or altered invoices go undetected without automated 3-way matching and anomaly detection.
- **Missed savings:** without automated payment-timing intelligence, early-payment discounts are missed and cash flow isn't optimized.
- **Slow approvals:** email/spreadsheet-based routing creates bottlenecks and no audit trail.

**Who feels this most:** AP clerks (manual burden), Controllers (audit/compliance risk), CFOs (spend visibility and cash flow).

---

## 3. Goals & Success Metrics


| Goal                                  | Metric                                       | Target `[Assumption]`                                                              |
| ------------------------------------- | -------------------------------------------- | ---------------------------------------------------------------------------------- |
| Reduce manual invoice processing time | Avg. minutes per invoice                     | From ~12 min → ≤3 min (human review only, not full re-entry)                       |
| Reduce duplicate/fraudulent payments  | $ caught by fraud detection / month          | Track from day 1; target ≥99% duplicate-catch rate                                 |
| Faster approvals                      | Avg. approval cycle time                     | From ~5 business days → ≤1.5 business days                                         |
| Budget adherence                      | % of spend within policy at time of approval | ≥95%                                                                               |
| Adoption                              | Weekly active AP users (of licensed seats)   | ≥80% by end of Q2 post-launch                                                      |
| AI extraction quality                 | Field-level accuracy on structured invoices  | ≥95%, with low-confidence fields routed to human review rather than silently wrong |


---

## 4. Users & Personas

1. **AP Clerk / Processor** — uploads invoices, resolves exceptions (stages 1, 4). Goal: clear queue fast without introducing errors. Frustration: repetitive manual keying. Technical comfort: moderate.
2. **Approver / Department Manager** — reviews routed approvals (stage 10). Goal: approve/reject quickly from mobile or email. Frustration: too many low-value approvals landing on their desk. Technical comfort: low-moderate — needs a frictionless approval UI (ideally one-click from a notification).
3. **Controller / Finance Lead** — sets policy & budget rules, reviews risk scoring and fraud alerts (stages 8, 9, 15). Goal: confidence that nothing slips through; auditable trail. Technical comfort: high, finance-domain expert.
4. **CFO / Executive** — views dashboard & reports, uses the AI Copilot for ad-hoc questions (stages 13, 14, 15). Goal: fast answers without waiting on the finance team to pull a report. Technical comfort: low — needs natural language, not raw data.
5. **System Admin** — configures ERP integration, user roles, thresholds (stage 12). Goal: integration "just works" and stays in sync. Technical comfort: high.

---

## 5. Scope

### 5.1 Phased Scope (mapped from your 15-stage workflow)


| #   | Stage                                                      | Phase                                      | Notes                                                                                                                        |
| --- | ---------------------------------------------------------- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| 1   | Capture (PDF, image, email, scan, mobile)                  | **MVP**                                    | Email forwarding + web upload first; native mobile capture can be a responsive web camera upload, not a separate app, for v1 |
| 2   | AI Extraction                                              | **MVP**                                    | Core value prop — must ship in v1                                                                                            |
| 3   | Validation                                                 | **MVP**                                    |                                                                                                                              |
| 4   | Duplicate Detection                                        | **MVP**                                    |                                                                                                                              |
| 5   | 3-Way Matching (PO ↔ GRN ↔ Invoice)                        | **Phase 2**                                | Requires reliable PO/GRN data from ERP integration first — sequencing risk if built before stage 12                          |
| 6   | AI Expense Categorization                                  | **MVP**                                    |                                                                                                                              |
| 7   | Analytics & Intelligence (anomaly/fraud pattern detection) | **Phase 2**                                | Needs data volume to be reliable; ship basic rules-based version in MVP, ML-based version in Phase 2                         |
| 8   | Policy & Budget Check                                      | **MVP**                                    | Rules-based, configurable per org                                                                                            |
| 9   | Risk Scoring (0–100 + explanation)                         | **Phase 2**                                | Depends on stage 7 maturity                                                                                                  |
| 10  | Approval Routing                                           | **MVP**                                    |                                                                                                                              |
| 11  | Payment Intelligence                                       | **Phase 3**                                |                                                                                                                              |
| 12  | ERP Integration                                            | **Phase 2**                                | `[Assumption]` QuickBooks Online first (most common in target segment), NetSuite second                                      |
| 13  | Real-Time Dashboard                                        | **MVP**                                    | Basic version; advanced widgets in Phase 2                                                                                   |
| 14  | AI Finance Copilot                                         | **Phase 3**                                | Needs data maturity + guardrails; highest-risk feature to ship early                                                         |
| 15  | Reports & Analytics                                        | **MVP** (basic) → **Phase 2** (full suite) | Spend/vendor/budget-vs-actual in MVP; savings/risk/audit reports in Phase 2                                                  |


### 5.2 Out of Scope for v1

- Native iOS/Android apps (mobile-responsive web only)
- ERP systems beyond QuickBooks Online and NetSuite
- Multi-currency support beyond USD `[Assumption — confirm if international customers are targeted]`
- Card/payment execution (FinGuard recommends and tracks payment timing but does not move money itself in v1 — reduces PCI/regulatory scope)

---

## 6. Functional Requirements (per MVP stage)

### Stage 1 — Capture

- **Inputs:** PDF, image (JPG/PNG), email forwarding to a per-org unique address, web upload, mobile browser camera capture
- **Requirements:** Max 25MB/file `[Assumption]`, multi-page PDF support, batch upload up to 50 files at once
- **Acceptance criteria:** A user can upload a multi-page PDF invoice and see it appear in the processing queue within 5 seconds

### Stage 2 — AI Extraction

- **Fields extracted:** Vendor, Invoice No., Date, Due Date, Line Items, Subtotal, Tax, Total
- **Requirements:** Confidence score per field; fields below 85% confidence `[Assumption]` are flagged for human review rather than auto-accepted
- **Acceptance criteria:** ≥95% field-level accuracy on machine-generated (non-scanned) invoices; low-confidence fields visibly highlighted in the review UI

### Stage 3 — Validation

- **Requirements:** Mandatory-field check (vendor, amount, date required), tax recalculation check against line items, date format normalization
- **Acceptance criteria:** An invoice missing a required field cannot proceed to approval without explicit override + reason logged

### Stage 4 — Duplicate Detection

- **Requirements:** Match on invoice number + vendor (exact), and fuzzy match on amount + date + vendor similarity (catches re-submitted invoices with a slightly altered invoice number)
- **Acceptance criteria:** ≥99% catch rate on exact duplicates in test set; fuzzy matches surfaced as a warning, not auto-blocked (avoid false-positive frustration)

### Stage 6 — AI Categorization

- **Requirements:** Configurable category taxonomy per org (default: Travel, Software, Office Supplies, Equipment, Utilities, Professional Services, Other); user corrections feed back into a per-org override table
- **Acceptance criteria:** ≥90% first-pass categorization accuracy after 30 days of an org's usage (allowing the feedback loop to adapt)

### Stage 8 — Policy & Budget Check

- **Requirements:** Per-department/category budget limits, configurable approval-required thresholds, hard policy rules (e.g. "no invoices from unregistered vendors")
- **Acceptance criteria:** An invoice exceeding its department's remaining monthly budget is flagged before reaching an approver

### Stage 10 — Approval Routing

- **Requirements:** Amount-based and department-based routing rules; sequential or parallel approval chains; one-click approve/reject from email or in-app notification
- **Acceptance criteria:** An approver can approve an invoice from a mobile email notification without logging into the full app

### Stage 13 — Real-Time Dashboard

- **Requirements:** Total spend, pending approvals, unpaid invoices, budget utilization — all live via WebSocket updates, not polling
- **Acceptance criteria:** Dashboard reflects a newly submitted invoice within 2 seconds without a manual refresh

*(Phase 2/3 stages — 5, 7, 9, 11, 12, 14, full 15 — get the same treatment once MVP scope is locked and build begins; use this section's format as the template.)*

---

## 7. Exceptions & Alerts Handling


| Exception         | Triggered by stage | Who resolves it                        | SLA `[Assumption]`        |
| ----------------- | ------------------ | -------------------------------------- | ------------------------- |
| Quantity Mismatch | 5                  | AP Clerk                               | 1 business day            |
| Price Mismatch    | 5                  | AP Clerk → Controller if >10% variance | 1 business day            |
| Tax Mismatch      | 5                  | AP Clerk                               | 1 business day            |
| Missing PO/GRN    | 5                  | AP Clerk (request from requester)      | 2 business days           |
| Duplicate Invoice | 4                  | AP Clerk                               | Same day (blocks payment) |
| Policy Violation  | 8                  | Controller                             | 1 business day            |
| Budget Exceeded   | 8                  | Controller / Department Manager        | 1 business day            |
| High Risk Score   | 9                  | Controller                             | Same day (holds payment)  |


All exceptions land in a single unified queue (not per-type inboxes) with filter/sort by type, age, and amount — avoids fragmenting AP clerk workflow across multiple views.

---

## 8. Non-Functional Requirements

### 8.1 Security & Compliance

- JWT access (15 min) + rotated refresh (7 days, HttpOnly cookie). Access token in `Authorization` header only — never in URLs. Refresh cookie: `HttpOnly; Secure; SameSite=Strict`; hashed at rest; reuse of a rotated token revokes all sessions for that user.
- Ownership-check pattern on every resource query — **org-scoped** (`organization_id`), not user-only. Wrong org → `404 NOT_FOUND` (do not leak existence). Wrong role, same org → `403 FORBIDDEN`.
- AES-256-GCM encryption for stored third-party tokens (ERP credentials)
- Immutable audit log: every state change (extraction override, approval, policy override) recorded with actor, timestamp, before/after values — required for stage 15's "Audit Trail" report and for any future SOC 2 effort
- Env validated at process start (crash if misconfigured). Standard JSON envelope `{ success, data }` / `{ success: false, error: { code, message, fields? } }`. API prefix `/api/v1`. `GET /health` + `GET /ready`. Rate limits on `/api` with stricter `/auth`. JSON body size cap separate from invoice multipart upload (25 MB).
- `[Assumption]` Compliance target: SOC 2 Type II readiness by end of Phase 2 (not required for MVP launch, but architecture — especially the audit log — must not require rework to get there). No PCI scope since FinGuard doesn't handle card data directly (see §5.2).

### 8.2 Performance

- `[Assumption]` Target volume: up to 2,000 invoices/day per org at MVP scale
- AI extraction latency: ≤10 seconds per single-page invoice, ≤30 seconds for multi-page
- Dashboard load: ≤2 seconds on initial load, real-time updates thereafter via WebSocket

### 8.3 Multi-tenancy

`[Assumption]` Multi-org SaaS from day one (not single-tenant deployments) — every collection/table includes an `organization_id`, and every query is scoped to it via the ownership-check pattern. This is the right default for a SaaS business model and is far more expensive to retrofit later than to build in from the start.

---

## 9. Technical Architecture

### 9.1 Stack Decision


| Layer                             | Choice                                                                                      | Rationale                                                                                                                                                |
| --------------------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Backend framework                 | **FastAPI** (Python) — primary recommendation                                               | Native async fits the AI/OCR-heavy workload (stages 2, 6, 7, 9, 14 all call external AI services); Pydantic validation; auto-generated OpenAPI docs      |
| Backend alternative               | Flask + Flask-Smorest                                                                       | Documented as a fallback if the build team has stronger Flask experience — same architecture patterns below apply with framework-specific syntax swapped |
| Frontend                          | React + Vite + TypeScript                                                                   | Unchanged regardless of backend language — talks to backend over HTTP/JSON + WebSocket                                                                   |
| Database                          | MongoDB Atlas + Beanie (async ODM) — **for MVP**                                            | Fast to iterate on evolving invoice/extraction schemas                                                                                                   |
| Database — reconsider for Phase 2 | PostgreSQL + SQLAlchemy                                                                     | Stage 5's 3-way matching (PO ↔ GRN ↔ Invoice) is inherently relational; revisit before building stage 5 rather than forcing it into Mongo                |
| Auth                              | Google OAuth + email/password, JWT (PyJWT) access + refresh rotation                        |                                                                                                                                                          |
| Real-time                         | FastAPI native WebSockets (or python-socketio if richer room/namespace features are needed) | Powers stage 13 live dashboard                                                                                                                           |
| Background jobs                   | Inline asyncio (default) or Celery + Redis when configured                                  | Extraction runs without Redis locally; Celery for production scale and Phase 2/3 schedules                                                               |
| AI/ML                             | See §10                                                                                     |                                                                                                                                                          |
| Deploy                            | Frontend: Vercel · Backend: Render/Railway · DB: MongoDB Atlas                              |                                                                                                                                                          |


### 9.2 Dependency versions (do not copy pins from this PRD)

Follow [`instruction.md`](instruction.md) **Version Safety Rule**: never treat a document table as the install source of truth.

- Authoritative ranges live in [`backend/pyproject.toml`](backend/pyproject.toml).
- Before adding or bumping a package: check PyPI (or `pip index versions <pkg>`) and search for advisories/CVEs.
- Prefer `>=` lower bounds on a supported major line, not stale exact pins from this file.
- **JWT:** PyJWT only — do **not** use `python-jose` (CVE-2024-33663 / low maintenance).
- **Passwords:** `bcrypt` directly — not passlib.
- Scaffold check (2026-08-23): FastAPI **0.141.1** was current on PyPI.

Frontend (when built): React, Vite, TypeScript, TanStack Query, Axios, React Hook Form + Zod, DOMPurify — verify npm latest + advisories the same way. Access token in memory only; never `localStorage`.

### 9.3 Repository & module structure

Monorepo: [`backend/`](backend/) first; `frontend/` later. Layout, middleware order, auth, and error codes: [`docs/BACKEND_PLANNING.md`](docs/BACKEND_PLANNING.md).

MVP modules: `auth`, `users`, `organizations`, `invoices`, `extraction`, `vendors`, `categories`, `policies`, `approvals`, `exceptions`, `audit`, `reports`. Phase 2/3: ERP, 3-way match, fraud ML, copilot.

### 9.4 Alignment with instruction.md

The blueprint in `instruction.md` is **Express 5 + TypeScript**. FinGuard’s runtime is **FastAPI + Pydantic** (PRD §9.1). Adopted practices: env crash-on-boot, envelope + error codes, JWT/refresh rotation, helmet-equivalent headers, CORS allowlist, rate limits, health/ready, structured logs without secrets, Postman collection, CI, `.env.example`, `.cursorignore`. Not adopted: Express/Mongoose/Zod/Passport package names, `userId`-only ownership (replaced by org + role), `10kb` JSON limit on file-upload routes.

---

## 10. AI/ML Requirements

- **Extraction (stage 2):** `[Assumption — needs your decision]` recommend evaluating AWS Textract or Google Document AI for structured OCR, with an LLM (e.g. Claude API) as a fallback for messy/handwritten invoices. Low-confidence fields (<85%) route to human review — never silently auto-accept.
- **Categorization (stage 6):** Default taxonomy above (§6), per-org override table populated from user corrections. Retrain/re-tune the categorization prompt or model monthly from accumulated corrections.
- **Risk Scoring (stage 9, Phase 2):** Start rules-based (weighted factors: new vendor, round-number amount, amount vs. historical average, velocity of submissions) with an LLM generating the human-readable "explanation" from the same factors — keeps the score auditable rather than a black box, which matters given it can block payment.
- **Fraud Pattern Detection (stage 7, Phase 2):** Duplicate-vendor-different-bank-details, round-number anomalies, velocity spikes (many invoices from a new vendor in a short window), new-vendor + high-amount combinations.
- **Finance Copilot (stage 14, Phase 3):** Scope to read-only queries against the org's own data (never cross-tenant). Guardrail: numeric answers must be generated by querying the actual database, not by the LLM inferring numbers from context — the LLM narrates a query result, it doesn't calculate one. Build test cases directly from the diagram's sample questions ("Which vendors have increased their prices?", "Find suspicious invoices.", etc.) before launch.

---

## 11. UX / UI Requirements

- `[Assumption]` Design system: clean, data-dense enterprise SaaS aesthetic consistent with the FinGuard brand (navy/teal gradient, shield motif) — not a playful consumer style, given the finance-professional audience.
- **Key screens:** Upload/capture, unified exception queue, approval inbox (mobile-optimized), risk score detail view (Phase 2), real-time dashboard, Copilot chat panel (Phase 3), reports (spend/vendor/budget-vs-actual).
- **Mobile:** Mobile-responsive web for v1, prioritizing the approval-inbox flow (approvers are the persona most likely to act from a phone) and camera-based capture upload. Native app deferred to a future phase pending demand.

---

## 12. Roles & Permissions


| Role             | Can do                                                                                                      |
| ---------------- | ----------------------------------------------------------------------------------------------------------- |
| Admin            | Full access: user management, integration config, policy/budget rule configuration, all financial data      |
| Controller       | Configure policies/budgets, resolve all exception types, view risk scores and fraud alerts, run all reports |
| Approver         | View and act on routed approvals within their department/amount authority only                              |
| AP Clerk         | Upload invoices, resolve extraction/duplicate exceptions, cannot approve payments or change policy          |
| Viewer / Auditor | Read-only access to invoices, transactions, and audit trail — no edit/approve rights                        |


---

## 13. Integrations


| Integration              | Priority                         | Notes                                                             |
| ------------------------ | -------------------------------- | ----------------------------------------------------------------- |
| QuickBooks Online        | **MVP-adjacent / Phase 2 start** | `[Assumption]` most common in target segment                      |
| NetSuite                 | Phase 2                          |                                                                   |
| Email ingestion          | MVP                              | Per-org unique forwarding address                                 |
| OCR/Document AI provider | MVP                              | Decision pending — see §10                                        |
| Payment rails (ACH)      | Phase 3                          | FinGuard recommends/tracks timing; does not execute payment in v1 |
| Google OAuth (SSO)       | MVP                              |                                                                   |


---

## 14. Release Plan

- **Phase 1 (MVP):** Backend-first. Stages 1, 2, 3, 4, 6, 8, 10, 13 + basic reporting (subset of 15). FastAPI + Mongo/Beanie. Extraction provider is pluggable (`mock` until OCR vendor is chosen). No ERP — unregistered-vendor and budget rules use vendors/budgets stored in FinGuard. Frontend after the API is stable.
- **Phase 2:** Stage 12 (ERP integration) → unlocks stage 5 (3-way matching, likely with a Postgres migration for the matching engine specifically) → stage 7 and 9 (fraud pattern detection, risk scoring) → full stage 15 reporting suite.
- **Phase 3:** Stage 11 (payment intelligence), stage 14 (AI Copilot) — the two highest-complexity, highest-trust-dependency features, deliberately sequenced last.

---

## 15. Risks & Assumptions

- **Technical risk:** OCR accuracy on scanned/handwritten invoices may fall well below the 95% target on machine-generated invoices — human-review fallback is not optional, it's load-bearing.
- **Technical risk:** Mongo → Postgres migration for stage 5 matching engine (if pursued) is nontrivial; better to decide before Phase 2 build starts than mid-build.
- **Business risk:** Trust in AI risk scores (stage 9) for payment-blocking decisions — an early false positive that blocks a legitimate payment could damage trust in the whole system. Mitigate by defaulting risk scoring to advisory-only (surfaces a flag, doesn't auto-block) until the model has a track record per org.
- **Business risk:** AI Copilot (stage 14) hallucinating financial figures is a severe trust failure for a finance product — hence the "narrate, don't calculate" guardrail in §10, and Phase 3 sequencing.
- **Assumption carried through this document:** multi-org SaaS, USD-only, QuickBooks-first ERP integration, SOC 2 as a Phase 2+ target. Any of these being wrong changes downstream scope meaningfully — confirm before build starts.

---

## 16. Open Questions

- OCR/LLM provider selection (§10) — needs a bake-off or vendor decision before stage 2 build starts
- International/multi-currency requirement — confirm if out of scope is correct
- SOC 2 timeline — does an early design partner require it sooner than "Phase 2+"?
- Native mobile app — revisit after MVP usage data shows how much approval activity happens on mobile web vs. desktop

---

## Appendix A — Naming & Brand Reference

- Product name: **FinGuard**
- Tagline: **Protect • Analyze • Optimize**
- Logo: shield + "FG" monogram + rising bar chart (navy → teal gradient)

## Appendix B — Related Documents

- [`docs/BACKEND_PLANNING.md`](docs/BACKEND_PLANNING.md) — FastAPI module structure, middleware, auth, env validation, error codes
- [`instruction.md`](instruction.md) — engineering/security blueprint (MERN syntax; practices ported to Python)
- Original workflow diagram — source of Section 5–7 structure

