import json

import pytest
from httpx import AsyncClient

from db.base import Base, engine_for_test, get_db, override_get_db
from main import app

Base.metadata.create_all(bind=engine_for_test)
app.dependency_overrides[get_db] = override_get_db
CLIENT = AsyncClient(base_url="http://127.0.0.1:8000", app=app)


@pytest.mark.asyncio
async def test_sign_up_해피케이스() -> None:
    async with CLIENT as ac:
        sing_up_data = {"name": "joo", "email": "joo@naver.com", "password": "p@ssword"}
        response = await ac.post("/users/sign_up", content=json.dumps(sing_up_data))
        result = response.json()
        assert result["name"] == "joo"
        assert result["email"] == "joo@naver.com"


# async def test_sign_up_이미_있는_유저일때() -> None:
#     async with CLIENT as ac:
#         sing_up_data = {"name": "test_joo", "email": "test_joo@naver.com", "password": "p@ssword"}
#         response = await ac.post("/users/sign_up", content=json.dumps(sing_up_data))

#         result = response.json()
#         assert result['name'] == "joo"
#         assert result['email'] == "joo@naver.com"
