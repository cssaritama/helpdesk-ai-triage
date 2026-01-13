# MCP Tool Server

This repository includes an MCP-style tool server that exposes operational tools for the helpdesk system.

## Why MCP here
MCP is used to define a tool interface that can be consumed by an LLM client or agent runtime. Tools map directly to backend capabilities:
- Create a ticket
- Run triage
- Search the knowledge base
- Suggest a reply

## How to run (docker-compose)
From repository root:
- `make up`
- MCP server is exposed at: `http://localhost:8765`

## Tools (HTTP interface)
This project implements an MCP-inspired tool registry over HTTP for simplicity and reproducibility.

- `GET /tools` -> lists tool schemas
- `POST /tools/{name}/invoke` -> invokes a tool

Example:
- `curl http://localhost:8765/tools`
- `curl -X POST http://localhost:8765/tools/create_ticket/invoke -H 'Content-Type: application/json' -d '{"title":"...","description":"..."}'`

## Notes for reviewers
- Tools are thin wrappers calling the backend API.
- The server returns structured JSON results for each tool call.
