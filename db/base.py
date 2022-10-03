from typing import AsyncIterable

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

DSN = "postgresql://joo:1234@127.0.0.1:5432/fast_api"
DSN_FOR_TEST = "postgresql://joo:1234@127.0.0.1:5432/test_fast_api"


engine_for_test = create_engine(DSN_FOR_TEST)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_for_test)


Base = declarative_base()


def override_get_db() -> AsyncIterable[Session]:
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine_for_test)


engine = create_engine(DSN)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db() -> AsyncIterable[Session]:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
