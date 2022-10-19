import hashlib
import json
from unittest import TestCase

from starlette.testclient import TestClient

from db.base import Base, get_db
from db_for_test.base import TestingSessionLocal, engine_for_test, override_get_db
from main import app
from routers.users.models import UserModel

HEADERS = {"Content-Type": "application/json; charset=utf-8"}

app.dependency_overrides[get_db] = override_get_db
Base.metadata.drop_all(engine_for_test)
Base.metadata.create_all(engine_for_test)


class TestUserAPI(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        db = TestingSessionLocal()

        hashed_password = hashlib.sha256("p@ssword".encode("utf-8")).hexdigest()
        new_user = UserModel(name="exist", email="exist@naver.com", password=hashed_password)

        db.add(new_user)
        db.commit()

    def test_sign_up_해피케이스(self) -> None:
        client = TestClient(base_url="http://127.0.0.1:8000", app=app)
        sign_up_data = {
            "name": "joo",
            "email": "joo@naver.com",
            "password": "p@ssword",
        }
        response = client.post("/users/sign_up", data=json.dumps(sign_up_data), headers=HEADERS)
        result = response.json()

        assert result["name"] == "joo"
        assert result["email"] == "joo@naver.com"

    def test_sign_up_이미_있는_유저일때(self) -> None:
        client = TestClient(base_url="http://127.0.0.1:8000", app=app)

        sign_up_data = {
            "name": "exist",
            "email": "exist@naver.com",
            "password": "p@ssword",
        }
        response = client.post("/users/sign_up", data=json.dumps(sign_up_data), headers=HEADERS)
        result = response.json()

        assert result["detail"][0]["msg"] == "이미 존재하는 이메일입니다."

    def test_sign_up_이메일이_아닐때(self) -> None:
        client = TestClient(base_url="http://127.0.0.1:8000", app=app)
        sign_up_data = {
            "name": "exist",
            "email": "existnaver.com",
            "password": "p@ssword",
        }
        response = client.post("/users/sign_up", data=json.dumps(sign_up_data), headers=HEADERS)
        result = response.json()
        assert result["detail"][0]["msg"] == "올바른 이메일 형식이 아닙니다."

    def test_sign_up_패스워드가_8자_이하일때(self) -> None:
        client = TestClient(base_url="http://127.0.0.1:8000", app=app)
        sign_up_data = {
            "name": "joo",
            "email": "joo@naver.com",
            "password": "p@sswor",
        }
        response = client.post("/users/sign_up", data=json.dumps(sign_up_data), headers=HEADERS)
        result = response.json()

        assert result["detail"][0]["msg"] == "비밀번호는 8자 이상이어야 합니다."
        assert response.status_code == 422

    def test_sign_up_패스워드에_특수문자가_없을때(self) -> None:
        client = TestClient(base_url="http://127.0.0.1:8000", app=app)
        sign_up_data = {
            "name": "joo",
            "email": "joo@naver.com",
            "password": "psssword",
        }
        response = client.post("/users/sign_up", data=json.dumps(sign_up_data), headers=HEADERS)
        result = response.json()

        assert result["detail"][0]["msg"] == "비밀번호는 특수문자를 포함해야 합니다."
        assert response.status_code == 422

    def test_sign_in_성공했을때(self) -> None:
        client = TestClient(base_url="http://127.0.0.1:8000", app=app)

        sign_in_data = {"email": "exist@naver.com", "password": "p@ssword"}

        response = client.post("/users/sign_in", data=json.dumps(sign_in_data), headers=HEADERS)

        result = response.json()

        assert response.status_code == 200
        assert "access_token" in result

    def test_sign_in_비밀번호가_틀렸을때(self) -> None:
        client = TestClient(base_url="http://127.0.0.1:8000", app=app)

        sign_in_data = {"email": "exist@naver.com", "password": "password@"}

        response = client.post("/users/sign_in", data=json.dumps(sign_in_data), headers=HEADERS)

        result = response.json()

        assert response.status_code == 404
        assert result["detail"][0]["msg"] == "이메일 혹은 비밀번호를 확인해주세요."

    def test_sign_in_없는_유저로_시도하려고_할때(self) -> None:
        client = TestClient(base_url="http://127.0.0.1:8000", app=app)

        sign_in_data = {"email": "not_exist@naver.com", "password": "p@ssword"}

        response = client.post("/users/sign_in", data=json.dumps(sign_in_data), headers=HEADERS)

        result = response.json()

        assert response.status_code == 404
        assert result["detail"][0]["msg"] == "이메일 혹은 비밀번호를 확인해주세요."

    def test_sign_in_이메일이_아닌_값을_넣었을때(self) -> None:
        client = TestClient(base_url="http://127.0.0.1:8000", app=app)

        sign_in_data = {"email": "joonavercom", "password": "p@ssword"}

        response = client.post("/users/sign_in", data=json.dumps(sign_in_data), headers=HEADERS)

        result = response.json()

        assert result["detail"][0]["msg"] == "올바른 이메일 형식이 아닙니다."
        assert response.status_code == 422
