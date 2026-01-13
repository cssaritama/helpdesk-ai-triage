# Architecture Diagrams (Textual)

## High-level architecture

User -> Frontend (React) -> Backend (FastAPI) -> Database (Postgres/SQLite)
                                     |
                                     +-> AI Services (LLM + Embeddings; mockable)
                                     |
                                     +-> KB Retrieval (vector or text search)
                                     |
                                     +-> MCP Tool Server (calls backend APIs)

## Request flow: triage + suggested reply

1. User creates a ticket via the UI.
2. UI calls `POST /tickets`.
3. User clicks "Run triage":
   - UI calls `POST /tickets/{id}/triage`.
   - Backend runs classification (LLM mock or real), persists triage.
4. User clicks "Suggest reply":
   - UI calls `POST /tickets/{id}/suggest-reply`.
   - Backend retrieves top-K KB hits, drafts reply, returns citations, persists suggestion.
