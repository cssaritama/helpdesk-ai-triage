# AI-Assisted Development Notes (AGENTS)

This project was built with explicit AI-assisted workflows, while maintaining deterministic tests and human review for critical changes.

## How AI tools were used
- Drafting initial architecture and API surface.
- Generating boilerplate scaffolding (project structure, Dockerfiles, workflows).
- Producing first-pass unit tests and integration test scenarios.
- Refining documentation to meet peer-review criteria.

## Human verification workflow
- Every AI-generated change is reviewed for correctness and security.
- API schemas and migrations are verified via automated tests.
- Deterministic modes are used for CI: no external LLM calls in test runs.

## Deterministic AI strategy
The system supports two modes:

1) `LLM_MODE=mock`, `EMBEDDINGS_MODE=mock` (default for tests and local docker-compose)
- Predictable outputs for classification and reply generation.
- Fully offline test execution.

2) `LLM_MODE=real`, `EMBEDDINGS_MODE=real` (production)
- Requires provider keys (e.g., OPENAI_API_KEY).
- Used only in deployed environments.

## Prompt and evaluation discipline
- Prompts are documented in `docs/ai/PROMPTS.md`.
- Core behaviors are validated by tests (triage schema validation, reply citations shape).
