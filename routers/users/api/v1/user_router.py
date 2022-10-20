from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config import JWT_SECRET_KEY
from db.base import Base, engine, get_db
from routers.users.services.user_info_service import (
    create_user_service,
    delete_user_service,
    get_user_service,
    update_user_service,
)

from .schemas.user_info_request import UserCreate, UserSignIn, UserUpdate
from .schemas.user_info_response import SignInResponse, UserResponse, UserUpdateResponse

Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/users")

HEADERS = {"Content-Type": "application/json; charset=utf-8"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def is_authenticate(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail=[{"msg": "로그인이 필요합니다."}], headers=HEADERS)
    token = authorization.split(" ", 1)[1]
    if not token:
        raise HTTPException(status_code=401, detail=[{"msg": "로그인이 필요합니다."}], headers=HEADERS)
    try:
        jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail=[{"msg": "만료된 토큰입니다."}], headers=HEADERS)


@router.post("/sign_up", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    try:
        create_user_service(db=db, user=user)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e, headers=HEADERS)
    except IntegrityError:
        raise HTTPException(status_code=400, detail=[{"msg": "이미 존재하는 이메일입니다."}], headers=HEADERS)
    return user


@router.post("/sign_in", response_model=SignInResponse, status_code=status.HTTP_200_OK)
async def sign_in(user: UserSignIn, db: Session = Depends(get_db)) -> SignInResponse:
    cur_user = get_user_service(db, user=user)
    if cur_user:
        payload = {
            "id": str(cur_user.email),
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 10),
        }
        token = jwt.encode(payload=payload, key=JWT_SECRET_KEY, algorithm="HS256")
        return {"msg": "로그인 성공", "access_token": token}
    raise HTTPException(status_code=404, detail=[{"msg": "이메일 혹은 비밀번호를 확인해주세요."}])


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserUpdateResponse,
    dependencies=[Depends(is_authenticate)],
)
async def update_user(
    user: UserUpdate,
    user_id: int,
    db: Session = Depends(get_db),
) -> UserUpdateResponse:
    try:
        message = update_user_service(db=db, user=user, user_id=user_id)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e, headers=HEADERS)
    return {"msg": message, "name": user.name}


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    message = delete_user_service(db=db, user_id=user_id)
    return {"detail": [{"msg": message}]}
