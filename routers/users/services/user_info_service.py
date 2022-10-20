import hashlib

from sqlalchemy import and_
from sqlalchemy.orm import Session

from routers.users.api.v1.schemas.user_info_request import UserCreate, UserSignIn, UserUpdate
from routers.users.models import UserModel


def get_user_service(db: Session, user: UserSignIn) -> UserModel:
    """
    db세션과 login_input을 받아와
    유저모델을 반환하는 서비스 함수
    """
    hashed_password = hashlib.sha256(user.password.encode("utf-8")).hexdigest()
    return (
        db.query(UserModel).filter(and_(UserModel.email == user.email, UserModel.password == hashed_password)).first()
    )


def get_user_by_id_service(db: Session, user_id: int) -> UserModel:
    """유저의 아이디값을 받아와 유저를 조회하는 함수

    :param db: db세션
    :type db: Session
    :param user_id: 유저의 프라이머리 키
    :type user_id: int
    :return: 아이디 값으로 조회된 유저인스턴스
    :rtype: UserModel
    """
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def create_user_service(db: Session, user: UserCreate) -> str:
    """
    db세션과 usercreate 스키마를 받아와
    유저데이터를 저장하고
    유저모델을 반환하는 서비스 함수
    """
    hashed_password = hashlib.sha256(user.password.encode("utf-8")).hexdigest()
    new_user = UserModel(name=user.name, email=user.email, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return "생성이 완료되었습니다."


def update_user_service(db: Session, user_id: int, user: UserUpdate) -> str:
    """
    db세션과 userupdate 스키마를 받아와
    유저데이터를 업데이트 하고
    유저모델을 반환하는 서비스 함수
    """
    cur_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if cur_user:
        for key, value in user.__dict__.items():
            if key == "password":
                value = hashlib.sha256(value.encode("utf-8")).hexdigest()
            setattr(cur_user, key, value)

        db.commit()
        db.refresh(cur_user)
        return "업데이트가 완료 되었습니다"
    raise


def delete_user_service(db: Session, user_id: int) -> str:
    """
    db세션과 user_id를 받아와
    유저를 삭제하고
    스테이터스 코드와 문자를 반환하는 서비스 함수
    """

    target_user = db.query(UserModel).filter_by(id=user_id).first()

    db.delete(target_user)
    db.commit()
    return "삭제 완료되었습니다."
