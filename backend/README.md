# Backend (FastAPI)

## Local development (without Docker)
1) Create venv
2) Install:
   - `pip install -e .[dev]`
3) Run migrations:
   - `alembic upgrade head`
4) Start:
   - `uvicorn app.main:app --reload`

## Environment
See `.env.example`.

## OpenAPI
- Served at `/openapi.json`
- Export snapshot:
  - `make gen-openapi` (from repo root)
