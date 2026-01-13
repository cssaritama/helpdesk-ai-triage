from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.tickets import router as tickets_router
from app.api.routes.kb import router as kb_router

app = FastAPI(
    title="Helpdesk AI Triage API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(tickets_router, prefix="/tickets", tags=["tickets"])
app.include_router(kb_router, prefix="/kb", tags=["knowledge_base"])
