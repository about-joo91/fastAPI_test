from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from db.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_date = Column(DateTime(timezone=True), onupdate=func.now())
