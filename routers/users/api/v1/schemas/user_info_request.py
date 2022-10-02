import re
from datetime import datetime

from pydantic import BaseModel, ValidationError, validator

REG = re.compile(r"[\@\#\$\%\^\&\*\(\)\-\_\=\+]")


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

    @validator("email")
    def email_must_contain_at(cls, v):
        if "@" not in v:
            raise ValidationError("올바른 이메일 형식이 아닙니다.")
        return v

    @validator("password")
    def password는_특수문자를_포함하고_8자이상이어야_한다(cls, v):
        if len(v) < 8:
            raise ValidationError("비밀번호는 8자 이상이어야 합니다.")
        if not REG.findall(v):
            raise ValidationError("비밀번호는 특수문자를 포함해야 합니다.")
        return v


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
