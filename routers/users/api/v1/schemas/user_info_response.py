from pydantic import BaseModel


class UserResponse(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class SignInResponse(BaseModel):

    access_token: str
