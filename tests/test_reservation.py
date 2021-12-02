import pytest
from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from starlette.routing import request_response
from src.reservation.main import app
from src.reservation.database import Base, get_db
from src.reservation.oauth2 import get_current_user
from src.reservation.models import User

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


def override_get_current_user():
    user_data = {
        "user_id": 1,
        "name": "foo",
        "surname": "rock",
        "citizen_id": "1152347583215",
        "birth_date": "2021-10-12",
        "occupation": "doctor",
        "address": "1145 bangkok",
        "password": "strong_password",
    }
    return User(**user_data)


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def store_user_in_db():
    user_data = {
        "name": "foo",
        "surname": "rock",
        "citizen_id": "1152347583215",
        "birth_date": "2021-10-12",
        "occupation": "doctor",
        "address": "1145 bangkok",
        "password": "strong_password",
    }
    # store user info in database
    client.post("/user/", json=user_data, headers={"Content-Type": "application/json"})


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

def create_reservation(timestamp):
    request_body = {"register_timestamp": timestamp}
    return client.post(
        "/reservation/", json=request_body, headers={"Content-Type": "application/json"}
    )

class TestGetAllReservation:

    def test_get_all_reservation_when_no_reservation_in_db(self, test_db):
        response = client.get("/reservation/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_reservation_when_db_has_one_reservation(self, test_db, store_user_in_db):
        create_reservation("2021-10-12T22:02:14.760Z")
        response = client.get("/reservation/")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["register_timestamp"] == "2021-10-12T22:02:14.760000"

    def test_get_all_reservation_when_db_has_many_reservation(self, test_db, store_user_in_db):
        create_reservation("2021-10-12T22:02:14.760Z")
        create_reservation("2021-10-12T22:02:14.760Z")
        create_reservation("2021-10-12T22:02:14.760Z")
        response = client.get("/reservation/")
        assert response.status_code == 200
        assert len(response.json()) == 3


class TestCreateReservation:

    def test_create_reservation_with_valid_request_body(self, test_db, store_user_in_db):
        request_body = {"register_timestamp": "2021-10-12T22:01:14.760Z"}
        response_body = {
            "reservation_id": 1,
            "register_timestamp": "2021-10-12T22:01:14.760000",
            "owner": {
                "name": "foo",
                "surname": "rock",
                "birth_date": "2021-10-12",
                "citizen_id": "1152347583215",
                "occupation": "doctor",
                "address": "1145 bangkok",
            },
            "vaccinated": False,
        }
        response = client.post(
            "/reservation/", json=request_body, headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 201
        assert response.json() == response_body

    def test_create_reservation_with_invalid_datetime_format(self, test_db, store_user_in_db):
        request_body = {"register_timestamp": "11/18/2021"}
        response = client.post(
            "/reservation/", json=request_body, headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "invalid datetime format"