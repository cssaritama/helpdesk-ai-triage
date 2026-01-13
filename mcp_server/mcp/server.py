from __future__ import annotations

import os
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException

BACKEND = os.getenv("MCP_BACKEND_BASE_URL", "http://localhost:8000").rstrip("/")

app = FastAPI(title="Helpdesk MCP Tool Server", version="1.0.0")

TOOLS: dict[str, dict[str, Any]] = {
    "create_ticket": {
        "description": "Create a new support ticket.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "requester_email": {"type": ["string", "null"]},
            },
            "required": ["title", "description"],
        },
    },
    "triage_ticket": {
        "description": "Run AI triage for a ticket.",
        "input_schema": {
            "type": "object",
            "properties": {"ticket_id": {"type": "string"}},
            "required": ["ticket_id"],
        },
    },
    "search_kb": {
        "description": "Search the knowledge base.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}, "k": {"type": "integer"}},
            "required": ["query"],
        },
    },
    "suggest_reply": {
        "description": "Draft a suggested reply for a ticket using KB retrieval.",
        "input_schema": {
            "type": "object",
            "properties": {"ticket_id": {"type": "string"}},
            "required": ["ticket_id"],
        },
    },
}

@app.get("/tools")
def list_tools() -> dict[str, Any]:
    return {"tools": [{"name": name, **spec} for name, spec in TOOLS.items()]}

@app.post("/tools/{name}/invoke")
def invoke_tool(name: str, payload: dict[str, Any]) -> dict[str, Any]:
    if name not in TOOLS:
        raise HTTPException(status_code=404, detail="Tool not found")

    with httpx.Client(timeout=10) as client:
        if name == "create_ticket":
            r = client.post(f"{BACKEND}/tickets", json=payload)
            r.raise_for_status()
            return {"result": r.json()}

        if name == "triage_ticket":
            ticket_id = payload["ticket_id"]
            r = client.post(f"{BACKEND}/tickets/{ticket_id}/triage")
            r.raise_for_status()
            return {"result": r.json()}

        if name == "search_kb":
            r = client.post(f"{BACKEND}/kb/search", json={"query": payload["query"], "k": payload.get("k", 5)})
            r.raise_for_status()
            return {"result": r.json()}

        if name == "suggest_reply":
            ticket_id = payload["ticket_id"]
            r = client.post(f"{BACKEND}/tickets/{ticket_id}/suggest-reply")
            r.raise_for_status()
            return {"result": r.json()}

    raise HTTPException(status_code=500, detail="Unhandled tool")
