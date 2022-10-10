import json
from unittest import IsolatedAsyncioTestCase

import pytest
from httpx import AsyncClient

from db.base import Base, get_db
from db_for_test.base import TestingSessionLocal, engine_for_test, override_get_db
from main import app
from routers.users.api.v1.schemas.user_info_request import UserCreate
from routers.users.models import UserModel


class TestUserAPI(IsolatedAsyncioTestCase):
    @classmethod
    async def asyncSetUp(cls) -> None:
        Base.metadata.create_all(bind=engine_for_test)

        app.dependency_overrides[get_db] = override_get_db

        db = TestingSessionLocal()

        user = UserCreate(name="exist", email="exist@naver.com", password="p@ssword")
        new_user = UserModel(name=user.name, email=user.email, password=user.password)

        db.add(new_user)
        db.commit()

    @pytest.mark.asyncio
    async def test_sign_up_해피케이스(self) -> None:
        async with AsyncClient(base_url="http://127.0.0.1:8000", app=app) as ac:
            sign_up_data = {
                "name": "joo",
                "email": "joo@naver.com",
                "password": "p@ssword",
            }
            response = await ac.post("/users/sign_up", content=json.dumps(sign_up_data))
            result = response.json()

            assert result["name"] == "joo"
            assert result["email"] == "joo@naver.com"

    @pytest.mark.asyncio
    async def test_sign_up_이미_있는_유저일때(self) -> None:
        async with AsyncClient(base_url="http://127.0.0.1:8000", app=app) as ac:
            sign_up_data = {
                "name": "exist",
                "email": "exist@naver.com",
                "password": "p@ssword",
            }
            response = await ac.post("/users/sign_up", content=json.dumps(sign_up_data))
            result = response.json()
            assert result["detail"] == "이미 존재하는 이메일입니다."

    async def asyncTearDown(self) -> None:
        Base.metadata.drop_all(bind=engine_for_test)
