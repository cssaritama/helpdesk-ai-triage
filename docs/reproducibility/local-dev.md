# Local Development (Without Docker)

Docker Compose is the reference environment for reproducibility and peer review. This document explains how to run locally without containers.

---

## 1) Backend (local)

### Prerequisites
- Python 3.11+
- pip
- (Optional) Postgres (recommended). SQLite also works.

### Setup
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .[dev]
cp .env.example .env
```

### Configure DB
SQLite (default):
- `DATABASE_URL=sqlite+pysqlite:///./app.sqlite3`

Postgres example:
- `DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DB`

### Run migrations and start the API
```bash
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

Verify:
```bash
curl http://localhost:8000/health
```

---

## 2) Frontend (local)

### Prerequisites
- Node.js 20+
- npm

### Setup and run
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open:
- http://localhost:5173

---

## 3) MCP server (local)

```bash
cd mcp_server
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
export MCP_BACKEND_BASE_URL=http://localhost:8000
uvicorn mcp.server:app --reload --port 8765
```

Verify:
```bash
curl http://localhost:8765/tools
```

---

## 4) Running tests locally

Backend:
```bash
cd backend
pytest -q
```

Frontend:
```bash
cd frontend
npm test
```

Integration tests expect the backend running and reachable at `BASE_URL`:
```bash
cd backend
BASE_URL=http://localhost:8000 pytest -q tests/integration
```
