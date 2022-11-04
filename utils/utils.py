import jwt
from fastapi import Header, HTTPException

from config import JWT_SECRET_KEY

HEADERS = {"Content-Type": "application/json; charset=utf-8"}


async def is_authenticated(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail=[{"msg": "로그인이 필요합니다."}], headers=HEADERS)
    token = authorization.split(" ", 1)[1]
    if not token:
        raise HTTPException(status_code=401, detail=[{"msg": "로그인이 필요합니다."}], headers=HEADERS)
    try:
        jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail=[{"msg": "만료된 토큰입니다."}], headers=HEADERS)
