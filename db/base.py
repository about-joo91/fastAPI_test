from typing import AsyncIterable

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

DSN = "postgresql://joo:1234@127.0.0.1:5432/fast_api"


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
