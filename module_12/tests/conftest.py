import os

# from aiohttp.pytest_plugin import *
import pymongo
import pytest
from asgiref.sync import sync_to_async
from faker import Faker
from pymongo.collection import Collection
from passlib.hash import pbkdf2_sha256

from module_12.todo_app.db import get_db
from module_12.todo_app.main import create_app as _create_app
from module_12.todo_app.settings import DB_URL

fake = Faker()

_TEST_DB = "test_todo_db"


def _init_db(db):
    users = [
        ("test", "test"),
    ]
    # todo remember to install pytest-aiohttp
    for user_tuple in users:
        username, password = user_tuple
        collection_name = f"todo_list_{username}_{fake.pystr(max_chars=5)}"
        db.user.insert_one(
            dict(
                username=username,
                password=pbkdf2_sha256.hash(password),
                todo_collection=collection_name,
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
            db_name=_TEST_DB,
            secret_key=os.urandom(32),
        ),
    )
    yield app


@pytest.fixture
def db(app):
    db = get_db(app)
    _init_db(db)
    yield db
    # cleanup after test
    db_url = DB_URL.format(_TEST_DB)
    mongo_client = pymongo.MongoClient(db_url)
    mongo_client.drop_database(app["config"]["db_name"])


@pytest.fixture
async def client(test_client, app):
    return await test_client(app)


class TestClient:
    def __init__(self, client, db):
        self._client = client
        self._db = db

    async def login(self, username="test", password="test"):
        return await self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    async def logout(self):
        return await self._client.get("/auth/logout")

    @property
    def client(self):
        return self._client

    @property
    def db(self):
        return self._db


@pytest.fixture(scope="function")
def test_helper(client, db):
    """Fixture to make access to db and client simpler"""
    return TestClient(client, db)


class UserCollectionHelper:
    def __init__(self, db):
        self._db = db

    @sync_to_async
    def _find_user_by_username(self, name):
        user_collection: Collection = self._db.user
        user = user_collection.find_one({"username": name})
        return user

    @sync_to_async
    def _find_all_users(self):
        user_collection: Collection = self._db.user
        find_all_users = list(user_collection.find())
        return find_all_users

    async def find_by_name(self, username):
        return await self._find_user_by_username(username)

    async def find_all_users(self):
        return await self._find_all_users()


@pytest.fixture(scope="function")
async def user_collection(db):
    """Helper fixture to get access to user collection"""
    return UserCollectionHelper(db)
