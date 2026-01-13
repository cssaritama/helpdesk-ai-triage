from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

def build_engine(database_url: str):
    connect_args = {}
    if database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    return create_engine(database_url, connect_args=connect_args, pool_pre_ping=True)

engine = build_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
