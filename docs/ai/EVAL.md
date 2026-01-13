# Evaluation Notes

## Key behaviors validated
- Triage output conforms to schema and is persisted.
- KB search returns stable ranking in mock embeddings mode.
- Suggested reply includes citations referencing existing KB articles.
- End-to-end integration: ticket -> triage -> KB -> reply.

## Non-goals (out of scope for the course project)
- PII detection/redaction (would be required for enterprise use).
- Advanced agentic orchestration (beyond MCP tool exposure).
