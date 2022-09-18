from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
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
from .schemas.user_info_response import SignInResponse, UserResponse

Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/users")


@router.post("/sign_up", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    create_user_service(db=db, user=user)
    return user


@router.post("/login", response_model=SignInResponse, status_code=status.HTTP_200_OK)
async def sign_in(user: UserSignIn, db: Session = Depends(get_db)) -> SignInResponse:
    cur_user = get_user_service(db, user=user)
    if cur_user:
        payload = {"id": str(cur_user.email), "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 10)}
        token = jwt.encode(payload=payload, key=JWT_SECRET_KEY, algorithm="HS256")
        return {"access_token": token}
    raise HTTPException(404, detail="이메일 혹은 비밀번호를 확인해주세요.")


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user: UserUpdate, user_id: int, db: Session = Depends(get_db)):
    detail = update_user_service(db=db, user=user, user_id=user_id)
    return {"detail": detail}


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    detail = delete_user_service(db=db, user_id=user_id)
    return {"detail": detail}
