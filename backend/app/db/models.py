from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

class KBArticle(Base):
    __tablename__ = "kb_articles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body_markdown: Mapped[str] = mapped_column(Text(), nullable=False)
    tags_json: Mapped[str] = mapped_column(Text(), nullable=False, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)

    @property
    def tags(self) -> list[str]:
        return json.loads(self.tags_json or "[]")

class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=False)
    requester_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="OPEN")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)

class TicketTriage(Base):
    __tablename__ = "ticket_triage"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_id: Mapped[str] = mapped_column(String(36), ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False)

    category: Mapped[str] = mapped_column(String(32), nullable=False)
    priority: Mapped[str] = mapped_column(String(8), nullable=False)
    sentiment: Mapped[str] = mapped_column(String(16), nullable=False)
    summary: Mapped[str] = mapped_column(Text(), nullable=False)
    suggested_tags_json: Mapped[str] = mapped_column(Text(), nullable=False, default="[]")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)

class TicketReplySuggestion(Base):
    __tablename__ = "ticket_reply_suggestions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_id: Mapped[str] = mapped_column(String(36), ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False)

    reply_markdown: Mapped[str] = mapped_column(Text(), nullable=False)
    citations_json: Mapped[str] = mapped_column(Text(), nullable=False, default="[]")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
