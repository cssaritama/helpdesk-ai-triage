# MCP Tool Server

This service exposes an MCP-inspired tool interface over HTTP.

- `GET /tools` lists tool schemas
- `POST /tools/{name}/invoke` invokes a tool

The server calls the backend API to execute operations and returns structured JSON results.
