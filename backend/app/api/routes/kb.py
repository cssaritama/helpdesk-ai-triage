from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.kb_repo import KBRepository
from app.schemas.kb import (
    KBArticleCreate,
    KBArticleOut,
    KBSearchRequest,
    KBSearchResponse,
    KBSearchHit,
)

router = APIRouter()

@router.post("/articles", response_model=KBArticleOut)
def create_article(payload: KBArticleCreate, db: Session = Depends(get_db)) -> KBArticleOut:
    repo = KBRepository(db)
    a = repo.create(payload.title, payload.body_markdown, payload.tags)
    return KBArticleOut(
        id=a.id,
        title=a.title,
        body_markdown=a.body_markdown,
        tags=a.tags,
        created_at=a.created_at,
    )

@router.get("/articles", response_model=list[KBArticleOut])
def list_articles(db: Session = Depends(get_db)) -> list[KBArticleOut]:
    repo = KBRepository(db)
    items = repo.list()
    return [
        KBArticleOut(id=a.id, title=a.title, body_markdown=a.body_markdown, tags=a.tags, created_at=a.created_at)
        for a in items
    ]

@router.get("/articles/{article_id}", response_model=KBArticleOut)
def get_article(article_id: str, db: Session = Depends(get_db)) -> KBArticleOut:
    repo = KBRepository(db)
    a = repo.get(article_id)
    if not a:
        raise HTTPException(status_code=404, detail="Article not found")
    return KBArticleOut(id=a.id, title=a.title, body_markdown=a.body_markdown, tags=a.tags, created_at=a.created_at)

@router.delete("/articles/{article_id}", response_model=dict)
def delete_article(article_id: str, db: Session = Depends(get_db)) -> dict:
    repo = KBRepository(db)
    a = repo.get(article_id)
    if not a:
        raise HTTPException(status_code=404, detail="Article not found")
    repo.delete(a)
    return {"deleted": True}

@router.post("/search", response_model=KBSearchResponse)
def search(payload: KBSearchRequest, db: Session = Depends(get_db)) -> KBSearchResponse:
    repo = KBRepository(db)
    hits = repo.naive_text_search(payload.query, payload.k)
    return KBSearchResponse(
        hits=[
            KBSearchHit(
                article=KBArticleOut(id=a.id, title=a.title, body_markdown=a.body_markdown, tags=a.tags, created_at=a.created_at),
                score=score,
            )
            for a, score in hits
        ]
    )
