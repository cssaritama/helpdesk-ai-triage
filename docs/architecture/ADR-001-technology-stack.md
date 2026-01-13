# ADR-001: Technology Stack

## Status
Accepted

## Context
The project must be reproducible, containerized, testable, and deployable, while demonstrating a realistic full-stack AI system.

## Decision
- Frontend: React + TypeScript + Vite
- Backend: FastAPI + SQLAlchemy 2.x + Alembic
- Database: SQLite for local dev; Postgres for production and integration tests
- AI layer:
  - LLM classification and reply drafting (pluggable; mock mode for tests)
  - Retrieval-augmented generation (KB search + citations)
- MCP:
  - A dedicated MCP-style tool server that exposes operational tools (ticket creation, triage, KB search, reply suggestion)
- Containerization: Docker + docker-compose for local parity
- CI/CD: GitHub Actions (tests, build, deploy)

## Consequences
- FastAPI provides OpenAPI spec generation as a first-class feature, enabling a contract-first workflow.
- SQLite lowers the barrier for contributors; Postgres ensures realistic behavior for integration tests and production.
- Mock AI mode guarantees deterministic test runs and eliminates dependency on external paid APIs.
