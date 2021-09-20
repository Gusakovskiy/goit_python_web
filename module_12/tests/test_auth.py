from random import choice

import pytest
from faker import Faker
from module_12.tests.conftest import UserCollectionHelper

fake = Faker()

password_length = [_id for _id in range(1, 13)]


@pytest.mark.parametrize(
    ("username", "password"),
    [(fake.name(), fake.pystr(max_chars=choice(password_length))) for _ in range(10)],
)
async def test_register(
    client,
    user_collection: UserCollectionHelper,
    db,
    username,
    password,
):
    response = await client.get("/auth/register")
    assert response.status == 200
    response = await client.post(
        "/auth/register",
        data={"username": username, "password": password},
        # follow_redirects=False,
    )
    # check redirect
    assert len(response.history)
    first_redirect = response.history[0]
    assert first_redirect.headers["Location"] == "/auth/login"

    test_user = await user_collection.find_by_name(username)
    assert test_user


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", "Username is required."),
        ("a", "", "Password is required."),
        ("test", "test", "Already registered."),
    ),
)
async def test_register_validate_input(client, db, username, password, message):
    response = await client.post(
        "/auth/register", data={"username": username, "password": password}
    )
    assert response.status == 200
    data = await response.text()
    assert message in data


async def test_login(db, test_helper):
    response = await test_helper.login()
    assert response.status == 200
    client = test_helper.client
    response = await client.get("/")
    assert response.status == 200
    app = client.app
    user = app["user"]
    assert user is not None
    assert user["username"] == "test"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    [
        ("a", "test", "Incorrect username."),
        ("test", fake.pystr(max_chars=1), "Incorrect password."),
        ("test", fake.pystr(max_chars=2), "Incorrect password."),
        ("test", fake.pystr(max_chars=4), "Incorrect password."),
        ("test", fake.pystr(max_chars=10), "Incorrect password."),
        ("test", fake.pystr(max_chars=12), "Incorrect password."),
    ],
)
async def test_login_validate_input(test_helper, db, username, password, message):
    response = await test_helper.login(username, password)
    assert response.status == 200
    data = await response.text()
    assert message in data


async def test_logout(test_helper):
    response = await test_helper.login()
    assert response.status == 200
    response = await test_helper.logout()
    assert response.status == 200
    user = test_helper.client.app.get("user")
    assert user is None
