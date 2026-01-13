from __future__ import annotations

from app.clients.llm_client import LLMClient
from app.schemas.ai import TriageResult

class TriageService:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, title: str, description: str) -> TriageResult:
        raw = self.llm.triage(title=title, description=description)
        return TriageResult(**raw)
