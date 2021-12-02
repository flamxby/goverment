from behave import *
from datetime import datetime
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

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

create_user_request1 = {
    "name": "foo",
    "surname": "rock",
    "birth_date": "2021-10-12",
    "occupation": "doctor",
    "address": "1145 bangkok",
    "password": "strong_password"
}
create_user_response1 = {}
catch_error1 = False

login_user_request = {}
login_user_response = {}

create_user_request2 = {
    "name": "foke",
    "surname": "rock",
    "birth_date": "2021-10-12",
    "occupation": "programmer",
    "address": "1145 bangkok",
    "password": "strong_password"
}
create_user_response2 = {}
catch_error2 = False

create_reservation_requset = {}
create_reservation_response = {}

get_reservation_response = {}

update_reservation_request = {}
update_reservation_response = {}

delete_reservation_response = {}

@given('create the test database')
def step_impl(context):
    Base.metadata.create_all(bind=engine)

@given('user1 input a citizen_id: "{text}" to create')
def step_impl(context, text):
    create_user_request1["citizen_id"] = text

@given('user2 input a citizen_id: "{text}" to create')
def step_impl(context, text):
    create_user_request2["citizen_id"] = text

@given('user1 input a password: "{text}" to create')
def step_impl(context, text):
    create_user_request1["password"] = text

@given('user2 input a password: "{text}" to create')
def step_impl(context, text):
    create_user_request2["password"] = text

@given('user1 input a citizen_id: "{text}" to login')
def step_impl(context, text):
    login_user_request["username"] = text

@given('user1 input a password: "{text}" to login')
def step_impl(context, text):
    login_user_request["password"] = text

@given('user1 input a timestamp: "{text}" to create reservation')
def step_impl(context, text):
    dt_obj = datetime.strptime(text, '%d/%m/%Y')
    create_reservation_requset["register_timestamp"] = dt_obj.isoformat()

@given('user1 input a new timestamp: "{text}" to update reservation')
def step_impl(context, text):
    dt_obj = datetime.strptime(text, '%d/%m/%Y')
    update_reservation_request["register_timestamp"] = dt_obj.isoformat()

@when('user1 send a request to update reservation id: "{text}"')
def step_impl(context, text):
    global update_reservation_response
    access_token = login_user_response.json().get("access_token")
    update_reservation_response = client.put(f"/reservation/{text}", json=update_reservation_request, headers={"Accept": "application/json", "Authorization": f"Bearer {access_token}"})

@when('user1 send a request to create reservation')
def step_impl(context):
    global create_reservation_response
    access_token = login_user_response.json().get("access_token")
    create_reservation_response = client.post("/reservation/", json=create_reservation_requset, headers={"Accept": "application/json", "Authorization": f"Bearer {access_token}"})

@when('user1 send a request to login')
def step_impl(context):
    global login_user_response
    login_user_response = client.post("/login", data=login_user_request, headers={"Content-Type": "application/x-www-form-urlencoded"})

@when('user1 send a request to create a user')
def step_impl(context):
    global create_user_response1
    create_user_response1 = client.post("/user/", json=create_user_request1, headers={'Content-Type': 'application/json'})

@when('user2 send a request to create a user')
def step_impl(context):
    global create_user_response2
    global catch_error2
    try:
        create_user_response2 = client.post("/user/", json=create_user_request2, headers={'Content-Type': 'application/json'})
    except exc.IntegrityError:
        catch_error2 = True

@when('user1 send a request to get a reservation id: "{text}"')
def step_impl(context, text):
    global get_reservation_response
    access_token = login_user_response.json().get("access_token")
    get_reservation_response = client.get(f"/reservation/{text}", headers={"Accept": "application/json", "Authorization": f"Bearer {access_token}"})

@when('user1 send a request to delete a reservation id: "{text}"')
def step_impl(context, text):
    global delete_reservation_response
    access_token = login_user_response.json().get("access_token")
    delete_reservation_response = client.delete(f"/reservation/{text}", headers={"Accept": "application/json", "Authorization": f"Bearer {access_token}"})

@then('website send status code "{text}" to user1 from get reservation')
def step_impl(context, text):
    assert int(text) == get_reservation_response.status_code

@then('website send status code "{text}" to user1')
def step_impl(context, text):
    assert int(text) == create_user_response1.status_code

@then('website send status code "{text}" to user2')
def step_impl(context, text):
    assert int(text) == create_user_response2.status_code

@then('website send status code "{text}" to user1 from login')
def step_impl(context, text):
    assert int(text) == login_user_response.status_code

@then('website send status code "{text}" to user1 from create reservation')
def step_impl(context, text):
    assert int(text) == create_reservation_response.status_code

@then('website send status code "{text}" to user1 from update reservation')
def step_impl(context, text):
    assert int(text) == update_reservation_response.status_code

@then('website send status code "{text}" to user1 from delete reservation')
def step_impl(context, text):
    assert int(text) == delete_reservation_response.status_code

@then('Has an error for create user2')
def step_impl(context):
    assert catch_error2 == True

@then('tear down database')
def step_impl(context):
    Base.metadata.drop_all(bind=engine)

