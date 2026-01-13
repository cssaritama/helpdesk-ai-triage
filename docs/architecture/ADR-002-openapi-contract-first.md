# ADR-002: OpenAPI as the Contract

## Status
Accepted

## Context
Peer evaluation requires an OpenAPI spec that reflects front-end requirements and acts as the contract for back-end development.

## Decision
- The backend is implemented in FastAPI and serves OpenAPI at `/openapi.json`.
- The repository exports a stable OpenAPI snapshot to `docs/api/openapi.yaml` via `make gen-openapi`.
- The frontend uses the exported OpenAPI snapshot to generate TypeScript types (`openapi-typescript`) and a typed client wrapper.

## Consequences
- Reviewers can validate the API contract independently of runtime services.
- Frontend-backend drift is minimized by regenerating types from the spec.
