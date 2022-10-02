import json

import pytest
from httpx import AsyncClient

from db.base import Base, get_db
from db_for_test.base import engine, override_get_db
from main import app

Base.metadata.create_all(bind=engine)
app.dependency_overrides[get_db] = override_get_db
CLIENT = AsyncClient(base_url="http://127.0.0.1:8000", app=app)


@pytest.mark.asyncio
async def test_sign_up_해피케이스() -> None:
    async with CLIENT as ac:
        sing_up_data = {"name": "joo", "email": "joo12345678@naver.com", "password": "p@ssword"}
        response = await ac.post("/users/sign_up", content=json.dumps(sing_up_data))

        print(response.json()["detail"])
        assert response.status_code == 400
        assert response.json()["detail"] == "이미 존재하는 이메일입니다."
