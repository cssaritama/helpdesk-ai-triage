from __future__ import annotations

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.ticket_repo import TicketRepository
from app.repositories.kb_repo import KBRepository
from app.schemas.ticket import TicketCreate, TicketOut, TicketListOut, TicketUpdateStatus
from app.schemas.ai import TriageOut, ReplySuggestionOut
from app.clients.llm_client import LLMClient
from app.services.triage_service import TriageService
from app.services.rag_service import RAGService

router = APIRouter()

@router.post("", response_model=TicketOut)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)) -> TicketOut:
    repo = TicketRepository(db)
    t = repo.create(title=payload.title, description=payload.description, requester_email=payload.requester_email)
    return TicketOut.model_validate(t.__dict__)

@router.get("", response_model=TicketListOut)
def list_tickets(status: str | None = None, db: Session = Depends(get_db)) -> TicketListOut:
    repo = TicketRepository(db)
    items = repo.list(status=status)
    return TicketListOut(items=[TicketOut.model_validate(i.__dict__) for i in items])

@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)) -> TicketOut:
    repo = TicketRepository(db)
    t = repo.get(ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return TicketOut.model_validate(t.__dict__)

@router.patch("/{ticket_id}/status", response_model=TicketOut)
def update_status(ticket_id: str, payload: TicketUpdateStatus, db: Session = Depends(get_db)) -> TicketOut:
    repo = TicketRepository(db)
    t = repo.get(ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    t = repo.update_status(t, payload.status)
    return TicketOut.model_validate(t.__dict__)

@router.post("/{ticket_id}/triage", response_model=TriageOut)
def triage_ticket(ticket_id: str, db: Session = Depends(get_db)) -> TriageOut:
    repo = TicketRepository(db)
    t = repo.get(ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")

    llm = LLMClient()
    svc = TriageService(llm)
    triage = svc.run(t.title, t.description)

    saved = repo.save_triage(
        ticket_id=t.id,
        category=triage.category,
        priority=triage.priority,
        sentiment=triage.sentiment,
        summary=triage.summary,
        tags=triage.suggested_tags,
    )

    out = {
        "id": saved.id,
        "ticket_id": saved.ticket_id,
        "category": saved.category,
        "priority": saved.priority,
        "sentiment": saved.sentiment,
        "summary": saved.summary,
        "suggested_tags": json.loads(saved.suggested_tags_json or "[]"),
        "created_at": saved.created_at,
    }
    return TriageOut(**out)

@router.post("/{ticket_id}/suggest-reply", response_model=ReplySuggestionOut)
def suggest_reply(ticket_id: str, db: Session = Depends(get_db)) -> ReplySuggestionOut:
    t_repo = TicketRepository(db)
    t = t_repo.get(ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")

    kb_repo = KBRepository(db)
    rag = RAGService(kb_repo)
    res = rag.suggest_reply(t.title, t.description, k=5)

    saved = t_repo.save_reply_suggestion(ticket_id=t.id, reply_markdown=res.reply_markdown, citations=res.citations)
    out = {
        "id": saved.id,
        "ticket_id": saved.ticket_id,
        "reply_markdown": saved.reply_markdown,
        "citations": json.loads(saved.citations_json or "[]"),
        "created_at": saved.created_at,
    }
    return ReplySuggestionOut(**out)
