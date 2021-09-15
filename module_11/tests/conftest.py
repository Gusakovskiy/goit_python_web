from itertools import chain

import pytest
from faker import Faker
from flask import g
from pymongo.collection import Collection
from werkzeug.security import generate_password_hash

from module_11.personal_app import create_app
from module_11.personal_app.db import get_db

fake = Faker()


def _init_db():
    db = get_db()
    users = [
        ('test', 'test'),
    ]

    faker_users = [
        (fake.name(), fake.pystr(max_chars=3))
        for _ in range(3)
    ]
    for user_tuple in chain(users, faker_users):
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
                    title=fake.text(max_nb_chars=100),
                    done=fake.pybool(),
                    description=fake.sentence(nb_words=6),
                    priority=fake.pyint(),
                )
                for _ in range(100)
            ]
        )


@pytest.fixture
def app():

    app = create_app({
        'TESTING': True,
        'DB_NAME': 'test_todo_db',
        'SECRET_KEY': b'test_secret',
    })

    with app.app_context():
        _init_db()

    yield app
    with app.app_context():
        get_db()
        g.mongo_client.drop_database(app.config['DB_NAME'])


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

