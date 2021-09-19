import os
from itertools import chain

import pytest
from faker import Faker
from pymongo.collection import Collection
from werkzeug.security import generate_password_hash

from module_12.todo_app.db import get_db
from module_12.todo_app.main import create_app as _create_app

fake = Faker()


def _init_db(db):
    users = [
        ('test', 'test'),
    ]
    for user_tuple in users:
        username, password = user_tuple
        collection_name = f'todo_list_{username}_{fake.pystr(max_chars=5)}'
        db.user.insert_one(
            dict(
                username=username,
                password=generate_password_hash(password),
                todo_collection=collection_name
            ),
        )
        user_todo: Collection = getattr(db, collection_name)
        user_todo.insert_many(
            [
                dict(
                    title=fake.text(max_nb_chars=120),
                    done=fake.pybool(),
                    description=fake.sentence(nb_words=6),
                    priority=fake.pyint(),
                )
                for _ in range(5)
            ]
        )


@pytest.fixture
def app(loop):
    app = _create_app(
        loop=loop,
        config=dict(
            db_name='test_todo_db',
            secret_key=os.urandom(32),
        ),
    )
    yield app


@pytest.fixture
def db(app):
    db = get_db(app)
    _init_db(db)
    yield db
    mongo_client = app['mongo_client']
    mongo_client.drop_database(app['config']['db_name'])


@pytest.fixture
def client(test_client, app):
    return test_client(app)


class AuthActions:
    def __init__(self, client):
        self._client = client

    async def login(self, username='test', password='test'):
        return await self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    async def logout(self):
        return await self._client.get('/auth/logout')


@pytest.fixture(scope='function')
def auth_test(client):
    return AuthActions(client)
