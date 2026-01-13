from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=3)
    requester_email: EmailStr | None = None

class TicketUpdateStatus(BaseModel):
    status: str = Field(pattern="^(OPEN|IN_PROGRESS|RESOLVED|CLOSED)$")

class TicketOut(BaseModel):
    id: str
    title: str
    description: str
    requester_email: str | None
    status: str
    created_at: datetime
    updated_at: datetime

class TicketListOut(BaseModel):
    items: list[TicketOut]
