from app.clients.llm_client import LLMClient
from app.services.triage_service import TriageService

def test_triage_mock_deterministic():
    svc = TriageService(LLMClient())
    res = svc.run("Payment failed", "My card payment is failing and I am frustrated.")
    assert res.category == "Billing"
    assert res.priority in {"P1","P2","P3","P4"}
    assert res.sentiment in {"negative","neutral","positive"}
    assert isinstance(res.suggested_tags, list)
