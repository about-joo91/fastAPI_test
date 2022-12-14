from pydantic import BaseModel


class UserResponse(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class SignInResponse(BaseModel):
    msg: str
    access_token: str


class UserUpdateResponse(BaseModel):
    msg: str
    name: str
