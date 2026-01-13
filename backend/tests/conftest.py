import os
import pytest
from sqlalchemy.orm import Session

from app.db.session import build_engine
from app.db.base import Base
from sqlalchemy.orm import sessionmaker

@pytest.fixture()
def db_session() -> Session:
    url = os.getenv("DATABASE_URL", "sqlite+pysqlite:///./test.sqlite3")
    engine = build_engine(url)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
