from sqlalchemy.orm import Session
from app.repositories.kb_repo import KBRepository

def test_naive_text_search_orders_by_score(db_session: Session):
    repo = KBRepository(db_session)
    a1 = repo.create("Reset password", "Use forgot password link", ["account"])
    a2 = repo.create("Billing payment", "Payment failed troubleshooting", ["billing"])
    hits = repo.naive_text_search("payment failed", 5)
    assert hits
    assert hits[0][0].id == a2.id
