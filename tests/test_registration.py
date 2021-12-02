import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from src.reservation.main import app
from src.reservation.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestRegistration:
    def test_registration_with_valid_request_body(self, test_db):
        user_data = {
            "name": "foo",
            "surname": "rock",
            "citizen_id": "1152347583215",
            "birth_date": "2021-10-12",
            "occupation": "doctor",
            "address": "1145 bangkok",
            "password": "strong_password"
        }
        response_body = {
            "user_id": 1,
            "name": "foo",
            "surname": "rock",
            "citizen_id": "1152347583215",
            "occupation": "doctor",
            "address": "1145 bangkok",
            "reservations": []
        }
        response = client.post("/user/", json=user_data, headers={'Content-Type': 'application/json'})
        assert response.status_code == 201
        assert response.json() == response_body

    def test_registration_with_duplicate_citizen_id(self, test_db):
        user_data_1 = {
            "name": "foo",
            "surname": "rock",
            "citizen_id": "1152347583215",
            "birth_date": "2021-10-12",
            "occupation": "doctor",
            "address": "1145 bangkok",
            "password": "strong_password"
        }
        user_data_2 = {
            "name": "kung",
            "surname": "rock",
            "citizen_id": "1152347583215",
            "birth_date": "2021-10-12",
            "occupation": "nurse",
            "address": "1140 bangkok",
            "password": "strong_password"
        }
        client.post("/user/", json=user_data_1, headers={'Content-Type': 'application/json'})
        with pytest.raises(exc.IntegrityError):
            client.post("/user/", json=user_data_2, headers={'Content-Type': 'application/json'})

    def test_registration_with_citizen_id_not_equal_13(self, test_db):
        user_data = {
            "name": "foo",
            "surname": "rock",
            "citizen_id": "112",
            "birth_date": "2021-10-12",
            "occupation": "doctor",
            "address": "1145 bangkok",
            "password": "strong_password"
        }
        response = client.post("/user/", json=user_data, headers={'Content-Type': 'application/json'})
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "citizen id must have 13 digits"

    def test_registration_with_citizen_id_not_a_digit(self, test_db):
        user_data = {
            "name": "foo",
            "surname": "rock",
            "citizen_id": "real citizen_id",
            "birth_date": "2021-10-12",
            "occupation": "doctor",
            "address": "1145 bangkok",
            "password": "strong_password"
        }
        response = client.post("/user/", json=user_data, headers={'Content-Type': 'application/json'})
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "citizen id must be a digit"

class TestGetUser:
    def test_get_user_and_user_is_exist_in_db(self, test_db):
        user_data = {
            "name": "foo",
            "surname": "rock",
            "citizen_id": "1152347583215",
            "birth_date": "2021-10-12",
            "occupation": "doctor",
            "address": "1145 bangkok",
            "password": "strong_password"
        }
        client.post("/user/", json=user_data, headers={'Content-Type': 'application/json'})
        response = client.get("/user/1152347583215")
        assert response.status_code == 200
        assert response.json()["citizen_id"] == "1152347583215"

    def test_get_user_and_user_is_not_exist_in_db(self, test_db):
        response = client.get("/user/1152347583215")
        assert response.status_code == 404
        assert response.json()["detail"] == "No user with this citizen id"

    def test_get_user_with_string_citizen(self, test_db):
        response = client.get("/user/string")
        assert response.status_code == 404
        assert response.json()["detail"] == "No user with this citizen id"
