from typing import AsyncIterable

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

DSN = "postgresql://joo:1234@127.0.0.1:5432/test_fast_api"


engine = create_engine(DSN, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def override_get_db() -> AsyncIterable[Session]:
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
