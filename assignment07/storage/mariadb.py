from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from models.relational import Base


DB_USER = "root"
DB_PASSWORD = "root123"
DB_HOST = "127.0.0.1"
DB_PORT = 3307
DB_NAME = "articles_db"


def get_engine() -> Engine:
    url = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    engine = create_engine(url, echo=False, future=True)
    return engine


def create_database_schema() -> None:
    """Create tables if they do not exist."""
    engine = get_engine()
    Base.metadata.create_all(engine)


def get_session() -> Session:
    engine = get_engine()
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return session_factory()
