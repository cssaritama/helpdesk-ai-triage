from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field

class TriageResult(BaseModel):
    category: str = Field(pattern="^(Billing|Technical|Account|Sales|Other)$")
    priority: str = Field(pattern="^(P1|P2|P3|P4)$")
    sentiment: str = Field(pattern="^(negative|neutral|positive)$")
    summary: str
    suggested_tags: list[str] = Field(default_factory=list)

class TriageOut(TriageResult):
    id: str
    ticket_id: str
    created_at: datetime

class ReplySuggestionResult(BaseModel):
    reply_markdown: str
    citations: list[str] = Field(default_factory=list)

class ReplySuggestionOut(ReplySuggestionResult):
    id: str
    ticket_id: str
    created_at: datetime
