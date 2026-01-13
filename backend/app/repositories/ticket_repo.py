from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.models import Ticket, TicketTriage, TicketReplySuggestion

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

class TicketRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, description: str, requester_email: str | None) -> Ticket:
        t = Ticket(title=title, description=description, requester_email=requester_email)
        self.db.add(t)
        self.db.commit()
        self.db.refresh(t)
        return t

    def list(self, status: str | None = None) -> list[Ticket]:
        stmt = select(Ticket).order_by(Ticket.created_at.desc())
        if status:
            stmt = stmt.where(Ticket.status == status)
        return list(self.db.execute(stmt).scalars().all())

    def get(self, ticket_id: str) -> Ticket | None:
        return self.db.get(Ticket, ticket_id)

    def update_status(self, ticket: Ticket, status: str) -> Ticket:
        ticket.status = status
        ticket.updated_at = utcnow()
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def save_triage(self, ticket_id: str, category: str, priority: str, sentiment: str, summary: str, tags: list[str]) -> TicketTriage:
        import json
        triage = TicketTriage(
            ticket_id=ticket_id,
            category=category,
            priority=priority,
            sentiment=sentiment,
            summary=summary,
            suggested_tags_json=json.dumps(tags),
        )
        self.db.add(triage)
        self.db.commit()
        self.db.refresh(triage)
        return triage

    def get_latest_triage(self, ticket_id: str) -> TicketTriage | None:
        stmt = select(TicketTriage).where(TicketTriage.ticket_id == ticket_id).order_by(TicketTriage.created_at.desc())
        return self.db.execute(stmt).scalars().first()

    def save_reply_suggestion(self, ticket_id: str, reply_markdown: str, citations: list[str]) -> TicketReplySuggestion:
        import json
        s = TicketReplySuggestion(ticket_id=ticket_id, reply_markdown=reply_markdown, citations_json=json.dumps(citations))
        self.db.add(s)
        self.db.commit()
        self.db.refresh(s)
        return s

    def get_latest_reply_suggestion(self, ticket_id: str) -> TicketReplySuggestion | None:
        stmt = select(TicketReplySuggestion).where(TicketReplySuggestion.ticket_id == ticket_id).order_by(TicketReplySuggestion.created_at.desc())
        return self.db.execute(stmt).scalars().first()
