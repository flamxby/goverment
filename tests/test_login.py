import pytest
import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jose import jwt
from dotenv import load_dotenv
from src.reservation.main import app
from src.reservation.database import Base, get_db

load_dotenv()

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

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

def test_login_with_valid_username_and_password(test_db):
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
    login_data = {
        "username": "1152347583215",
        "password": "strong_password"
    }
    response = client.post('/login', data=login_data)
    assert response.status_code == 200
    token = response.json().get("access_token")
    credential = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert credential["sub"] == login_data["username"]