from random import choice

import pytest
from faker import Faker
from flask import g, session
from pymongo.database import Collection

from module_11.personal_app.db import get_db

fake = Faker()

password_length = [_id for _id in range(1, 13)]


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture(scope='function')
def auth(client):
    return AuthActions(client)


@pytest.mark.parametrize(('username', 'password'), [
    (fake.name(), fake.pystr(max_chars=choice(password_length)))
    for _ in range(10)
])
def test_register(username, password, client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': username, 'password': password}
    )
    # check redirect
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        db = get_db()
        user_collection: Collection = db.user
        test_user = user_collection.find_one({'username': username})
        assert test_user


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'Already registered.'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert response.status_code == 200
    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(
    ('username', 'password', 'message'),
    [
        ('a', 'test', b'Incorrect username.'),
        ('test', fake.pystr(max_chars=1), b'Incorrect password.'),
        ('test', fake.pystr(max_chars=2), b'Incorrect password.'),
        ('test', fake.pystr(max_chars=10), b'Incorrect password.'),
        ('test', fake.pystr(max_chars=12), b'Incorrect password.'),
    ] +
    [
        ('test', fake.pystr(max_chars=4).lower(),  b'Incorrect password.')  # bruteforce test user
        for _ in range(10)
    ]
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()
    with client:
        auth.logout()
        assert 'user_id' not in session
