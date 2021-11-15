import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
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


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


def create_reservation(timestamp):
    request_body = {"register_timestamp": timestamp}
    return client.post(
        "/reservation/", json=request_body, headers={"Content-Type": "application/json"}
    )


def test_create_reservation_with_valid_request_body(test_db):
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


def test_get_reservation_on_specific_date(test_db):
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
    # create reservation 1
    create_reservation("2021-10-12T22:01:14.760Z")
    response_body = [
        {
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
        },
        {
            "reservation_id": 2,
            "register_timestamp": "2021-10-12T22:02:14.760000",
            "owner": {
                "name": "foo",
                "surname": "rock",
                "birth_date": "2021-10-12",
                "citizen_id": "1152347583215",
                "occupation": "doctor",
                "address": "1145 bangkok",
            },
            "vaccinated": False,
        },
    ]
    # create reservation 2
    create_reservation("2021-10-12T22:02:14.760Z")
    # create reservation 3
    create_reservation("2021-10-13T22:02:14.760Z")
    response = client.get("/reservation/2021/10/12")
    assert response.status_code == 200
    assert response.json() == response_body
