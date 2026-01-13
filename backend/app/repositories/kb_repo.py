from __future__ import annotations

import math
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.models import KBArticle

class KBRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, body_markdown: str, tags: list[str]) -> KBArticle:
        import json
        a = KBArticle(title=title, body_markdown=body_markdown, tags_json=json.dumps(tags))
        self.db.add(a)
        self.db.commit()
        self.db.refresh(a)
        return a

    def get(self, article_id: str) -> KBArticle | None:
        return self.db.get(KBArticle, article_id)

    def list(self) -> list[KBArticle]:
        stmt = select(KBArticle).order_by(KBArticle.created_at.desc())
        return list(self.db.execute(stmt).scalars().all())

    def delete(self, article: KBArticle) -> None:
        self.db.delete(article)
        self.db.commit()

    def naive_text_search(self, query: str, k: int) -> list[tuple[KBArticle, float]]:
        # A deterministic fallback scoring for reproducible tests.
        # Score: token overlap / (1 + length penalty)
        q = set([t for t in query.lower().split() if t.strip()])
        results: list[tuple[KBArticle, float]] = []
        for a in self.list():
            tokens = set([t for t in (a.title + " " + a.body_markdown).lower().split() if t.strip()])
            overlap = len(q.intersection(tokens))
            denom = 1.0 + math.log(2.0 + len(tokens))
            score = float(overlap) / denom
            if score > 0:
                results.append((a, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]
