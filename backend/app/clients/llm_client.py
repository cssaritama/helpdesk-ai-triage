from __future__ import annotations

from app.core.config import settings

class LLMClient:
    """LLM client abstraction.

    In mock mode, returns deterministic outputs for tests.
    In real mode, you can implement provider calls (OpenAI-compatible).
    """

    def triage(self, title: str, description: str) -> dict:
        if settings.llm_mode == "mock":
            text = (title + " " + description).lower()
            if any(x in text for x in ["charge", "payment", "invoice", "billing"]):
                category = "Billing"
                priority = "P2"
            elif any(x in text for x in ["crash", "error", "bug", "fails", "not working"]):
                category = "Technical"
                priority = "P1"
            elif any(x in text for x in ["password", "login", "account"]):
                category = "Account"
                priority = "P2"
            elif any(x in text for x in ["pricing", "quote", "purchase"]):
                category = "Sales"
                priority = "P3"
            else:
                category = "Other"
                priority = "P3"

            sentiment = "negative" if any(x in text for x in ["angry", "frustrated", "hate", "terrible"]) else "neutral"
            summary = (description.strip()[:160] + "...") if len(description.strip()) > 160 else description.strip()
            tags = list({category.lower(), priority.lower()})
            return {
                "category": category,
                "priority": priority,
                "sentiment": sentiment,
                "summary": summary or "No description provided.",
                "suggested_tags": tags,
            }

        raise NotImplementedError("Real LLM mode is not implemented in this template. See docs/ for guidance.")
