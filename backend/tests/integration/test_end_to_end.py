import os
import time
import httpx

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

def wait_for_health(timeout_s: int = 30) -> None:
    start = time.time()
    while time.time() - start < timeout_s:
        try:
            r = httpx.get(f"{BASE_URL}/health", timeout=2)
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError("Backend did not become healthy in time")

def test_end_to_end_workflow():
    wait_for_health()

    # Create KB
    kb = httpx.post(
        f"{BASE_URL}/kb/articles",
        json={"title":"Password reset", "body_markdown":"Use forgot password", "tags":["account"]},
        timeout=10,
    )
    assert kb.status_code == 200
    kb_id = kb.json()["id"]

    # Create ticket
    t = httpx.post(
        f"{BASE_URL}/tickets",
        json={"title":"Cannot login", "description":"I forgot my password and cannot login", "requester_email":"a@b.com"},
        timeout=10,
    )
    assert t.status_code == 200
    ticket_id = t.json()["id"]

    # Triage
    tri = httpx.post(f"{BASE_URL}/tickets/{ticket_id}/triage", timeout=10)
    assert tri.status_code == 200
    assert tri.json()["category"] == "Account"

    # Reply suggestion
    rep = httpx.post(f"{BASE_URL}/tickets/{ticket_id}/suggest-reply", timeout=10)
    assert rep.status_code == 200
    data = rep.json()
    assert "reply_markdown" in data
    assert isinstance(data["citations"], list)
    # citation may or may not include kb_id depending on scoring, but should be well-formed
