# Helpdesk AI Triage + Knowledge Base

A production-style, full-stack AI helpdesk system that automates ticket triage and grounds suggested replies in an internal knowledge base.

This repository is engineered for peer-review evaluation criteria: clear problem description, AI-assisted development (including MCP), explicit architecture, OpenAPI contract, structured frontend/backend, persistent database support, containerization, unit + integration tests, deployment, CI/CD, and reproducibility.

---

## Problem Statement

Support teams in small and mid-sized organizations commonly face:

1. High ticket volumes with limited capacity (triage becomes a bottleneck).
2. Inconsistent prioritization (incorrect escalation and SLA breaches).
3. Fragmented knowledge and repeated work (solutions scattered across docs and memory).
4. Slow onboarding (new agents need constant senior support).

These issues increase operational cost and reduce customer satisfaction.

---

## Objectives

This project delivers an AI-assisted helpdesk system that:

- Automatically triages tickets into category/priority/sentiment with a short summary and tags.
- Retrieves relevant knowledge-base articles to ground decisions (RAG-style retrieval).
- Produces a suggested reply with citations to KB articles.
- Persists tickets, triage outputs, KB articles, and suggestions for auditability.
- Exposes capabilities via OpenAPI and via an MCP-style tool server for agent workflows.
- Fully reproducible: deterministic mock AI for CI and tests. A real-provider mode is planned; `backend/app/clients/llm_client.py` does not implement it yet, and triage uses keyword rules.

---

## System Overview

### Core features
- Ticket CRUD + status updates
- AI triage endpoint (`/tickets/{id}/triage`)
- KB CRUD + search (`/kb/articles`, `/kb/search`)
- Suggested reply endpoint grounded on KB (`/tickets/{id}/suggest-reply`)
- MCP-style tool server exposing operational tools over HTTP

### Technology stack
- Frontend: React + TypeScript (Vite)
- Backend: FastAPI + SQLAlchemy 2.x + Alembic
- Database: SQLite (dev) and Postgres (docker-compose / production-like)
- MCP tool server: FastAPI HTTP tool registry (MCP-inspired)
- Containerization: Docker + docker-compose
- CI: GitHub Actions runs the tests. The Cloud Run workflow is a template and does not deploy yet.

Architecture details: `docs/architecture/*`

---

## Reproducibility (Step-by-step)

If a reviewer follows the steps below on a clean machine with Docker installed, they should be able to run the full system end-to-end.

### A) One-command run (recommended: Docker Compose)

Prerequisites:
- Docker Engine / Docker Desktop
- Docker Compose v2
- (Optional) `make` (if not available, use the docker commands shown below)

1) Start the full system
- With Make:
  - `make up`
- Without Make:
  - `docker compose up --build -d`

2) Verify services are up
- `docker compose ps`
Expected:
- `frontend` exposed on `5173`
- `backend` exposed on `8000`
- `mcp` exposed on `8765`
- `db` exposed on `5432`

3) Verify backend health
- `curl http://localhost:8000/health`
Expected:
- `{"status":"ok"}`

4) Open the UI
- Frontend: http://localhost:5173

5) (Optional) Seed the Knowledge Base
- With Make:
  - `make seed`
- Without Make:
  - `python scripts/seed_kb.py`

6) Stop and clean volumes
- With Make:
  - `make down`
- Without Make:
  - `docker compose down -v`

### B) End-to-end API demo (copy/paste)

Run after starting the system:

1) Create a KB article
```bash
curl -s -X POST http://localhost:8000/kb/articles \
  -H 'Content-Type: application/json' \
  -d '{"title":"Password Reset","body_markdown":"Use Forgot Password.","tags":["account"]}'
```

2) Create a ticket
```bash
TICKET_ID=$(curl -s -X POST http://localhost:8000/tickets \
  -H 'Content-Type: application/json' \
  -d '{"title":"Cannot login","description":"I forgot my password and cannot login","requester_email":"user@example.com"}' | python -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "$TICKET_ID"
```

3) Run triage
```bash
curl -s -X POST "http://localhost:8000/tickets/${TICKET_ID}/triage"
```

4) Suggest a grounded reply
```bash
curl -s -X POST "http://localhost:8000/tickets/${TICKET_ID}/suggest-reply"
```

### C) Local development (without Docker)

Local dev is supported but Docker is the reference for reproducibility.
See `docs/reproducibility/local-dev.md`.

---

## Quickstart (Docker)

1) Start
- `make up`

2) Open
- UI: http://localhost:5173
- API: http://localhost:8000
- MCP: http://localhost:8765/tools

3) Stop
- `make down`

---

## API Contract (OpenAPI)

- Runtime: `GET /openapi.json`
- Snapshot committed for review: `docs/api/openapi.yaml`

Re-export snapshot:
- `make gen-openapi` (writes `docs/api/openapi.yaml`)

Frontend type generation (from the snapshot):
- `cd frontend && npm run gen:api`

---

## Testing (Step-by-step)

### Backend unit tests (fast, offline)
- `make test-backend`
Or:
- `cd backend && python -m pytest -q`

### Frontend tests
- `make test-frontend`
Or:
- `cd frontend && npm install && npm test`

### Integration tests (real Postgres, separated from unit tests)
These tests validate the full workflow and database persistence.

- With Make:
  - `make test-integration`

What it does:
1) Starts Postgres + backend (test settings)
2) Waits for `/health`
3) Executes end-to-end workflow:
   KB article → ticket → triage → suggested reply
4) Tears down containers and volumes

---

## AI Modes

### Mock mode (default for docker-compose and CI)
- `LLM_MODE=mock`
- `EMBEDDINGS_MODE=mock`

Properties:
- Deterministic outputs
- No external dependencies
- Suitable for unit/integration tests and peer-review reproducibility

### Real provider mode (planned, not implemented)
- `LLM_MODE=real`, `EMBEDDINGS_MODE=real`
- Provide provider credentials (e.g., `OPENAI_API_KEY`)

Prompts and the real-mode interface contract are documented in `docs/ai/PROMPTS.md`.

---

## MCP Tool Server

The MCP-inspired tool server exposes operational tools over HTTP:
- `GET /tools` — list tools
- `POST /tools/{name}/invoke` — invoke tool

Docs: `docs/mcp/README.md`

---

## Deployment

Guide:
- `docs/deployment/cloud-run.md`

Deployment status: not deployed. When it is, add a screenshot of a successful request at
`docs/deployment/cloud-run-proof.png`.

---

## CI/CD

- `.github/workflows/ci.yml` runs backend + frontend tests on push/PR.
- `.github/workflows/deploy-cloud-run.yml` is a template: it runs on push to `main` but only prints placeholders until authentication and deployment steps are added.

---

## Where each rubric item is covered

- Problem description: this README (problem, objectives, solution, expected behavior)
- AI system development + MCP: `docs/ai/*`, `docs/mcp/*`, `mcp_server/`
- Architecture: `docs/architecture/*`
- OpenAPI contract: `docs/api/openapi.yaml`
- Frontend: `frontend/src/*` + `frontend/src/tests/*`
- Backend: `backend/app/*` + `backend/tests/*`
- Database: Alembic migrations + SQLite/Postgres support
- Containerization: Dockerfiles + docker-compose
- Integration tests: `backend/tests/integration/*`
- Deployment: `docs/deployment/cloud-run.md` + screenshot requirement
- CI/CD: `.github/workflows/*`
- Reproducibility: this README + `docs/reproducibility/*` + Makefile

---

## License
MIT
