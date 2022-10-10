from typing import AsyncIterable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DSN_FOR_TEST = "postgresql://joo:1234@127.0.0.1:5432/test_fast_api"

engine_for_test = create_engine(DSN_FOR_TEST)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_for_test)


def override_get_db() -> AsyncIterable[Session]:
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
