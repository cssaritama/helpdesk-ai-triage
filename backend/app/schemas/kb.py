from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field

class KBArticleCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    body_markdown: str = Field(min_length=3)
    tags: list[str] = Field(default_factory=list)

class KBArticleOut(BaseModel):
    id: str
    title: str
    body_markdown: str
    tags: list[str]
    created_at: datetime

class KBSearchRequest(BaseModel):
    query: str = Field(min_length=2)
    k: int = Field(default=5, ge=1, le=20)

class KBSearchHit(BaseModel):
    article: KBArticleOut
    score: float

class KBSearchResponse(BaseModel):
    hits: list[KBSearchHit]
