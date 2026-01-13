from __future__ import annotations

from app.schemas.ai import ReplySuggestionResult
from app.repositories.kb_repo import KBRepository

class RAGService:
    """Retrieval-augmented reply suggestion.

    - retrieves top-K KB hits
    - drafts a reply (mock deterministic; can be replaced with real LLM)
    """

    def __init__(self, kb_repo: KBRepository):
        self.kb_repo = kb_repo

    def suggest_reply(self, ticket_title: str, ticket_description: str, k: int = 5) -> ReplySuggestionResult:
        hits = self.kb_repo.naive_text_search(f"{ticket_title} {ticket_description}", k=k)
        citations = [a.id for a, _ in hits]
        guidance = ""
        if hits:
            top = hits[0][0]
            guidance = f"\n\n---\nRelevant KB: **{top.title}**\n"

        reply = (
            "Hello,\n\n"
            "Thank you for reaching out. Based on your description, here are the recommended next steps:\n\n"
            "1. Follow the KB guidance relevant to your issue.\n"
            "2. If the problem persists, reply with additional context (screenshots/logs) so we can investigate.\n\n"
            "Best regards,\nSupport Team"
            + guidance
        )

        return ReplySuggestionResult(reply_markdown=reply, citations=citations)
