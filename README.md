# FinGuard

AI-powered invoice and expense management. **Backend first** — the API lives in [`backend/`](backend/). Frontend is deferred.

- Product: [`Finguard_prd.md`](Finguard_prd.md)
- Architecture: [`docs/BACKEND_PLANNING.md`](docs/BACKEND_PLANNING.md)
- API Reference & Scenarios: [`docs/API_DOCUMENTATION.md`](docs/API_DOCUMENTATION.md)
- Engineering practices: [`instruction.md`](instruction.md) (patterns applied on FastAPI, not Express)

## Quick start

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -e ".[dev]"
copy .env.example .env
# Set MONGODB_URI and JWT secrets (see .env.example)
uvicorn app.main:app --reload --port 5000
```

- Health: `GET http://localhost:5000/health`
- OpenAPI: `http://localhost:5000/docs`
- Postman: [`backend/postman/`](backend/postman/)

## CI

GitHub Actions runs lint-free pytest (unit tests). API tests that need Mongo are skipped unless `MONGODB_URI` is set.
