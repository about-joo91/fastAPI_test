from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    name: str
    email: str
    password: str
    is_active: bool
    created_date: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):

    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


class UserSignIn(BaseModel):

    email: str
    password: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: str | None
    password: str | None

    class Config:
        orm_mode = True
