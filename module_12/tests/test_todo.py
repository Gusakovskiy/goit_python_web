from random import randint

import pytest
from asgiref.sync import sync_to_async
from bson import ObjectId
from faker import Faker
from pymongo.collection import Collection

_FAKE_TASK_ID = str(ObjectId())
fake = Faker()


def _get_test_user_collection(db) -> Collection:
    user_collection: Collection = db.user
    test_user = user_collection.find_one({'username': 'test'})
    return getattr(db, test_user['todo_collection'])


def _generate_task(join_number):
    result = []
    for _ in range(join_number):
        result.append(fake.text(max_nb_chars=randint(10, 120)))
    return ';'.join(result)


@sync_to_async
def _get_task(db, query):
    todo_collection: Collection = _get_test_user_collection(db)
    todo = todo_collection.find_one(query)
    return todo


@sync_to_async
def _get_max_priority(db):
    todo_collection: Collection = _get_test_user_collection(db)
    max_priority = list(todo_collection.aggregate(
        [
            {
                "$group": {
                    "_id": None,
                    "max_priority": {"$max": "$priority"}
                }
            },
        ]
    ))[0]
    return max_priority['max_priority']


async def test_index(auth_test):
    client = auth_test.client
    response = await client.get('/')
    assert response.status == 200
    data = await response.text()
    assert "Log In" in data
    assert "Register" in data

    await auth_test.login()
    response = await client.get('/')

    assert response.status == 200
    data = await response.text()
    assert 'Log Out' in data


@pytest.mark.parametrize('path', (
        '/create',
        f'/{_FAKE_TASK_ID}/mark_done',
        f'/{_FAKE_TASK_ID}/delete',
))
async def test_login_required(client, path):
    response = await client.post(path)
    assert response.status == 200
    assert len(response.history) == 1
    redirect = response.history[0]
    assert redirect.headers['Location'] == '/auth/login'


@pytest.mark.parametrize('path', (
        f'/todo/{_FAKE_TASK_ID}/delete',
        f'/todo/{_FAKE_TASK_ID}/mark_done',
        '/todo/asdasdf/mark_done',
        '/todo/asdasdf/delete',
        # non existing url
        f'/todo/{_FAKE_TASK_ID}/delete/',
))
async def test_exists_required(auth_test, path):
    await auth_test.login()
    client = auth_test.client
    response = await client.post(path)
    assert response.status == 404


@pytest.mark.parametrize('done', (
        True,
        False,
))
async def test_mark_done(auth_test, done):
    client = auth_test.client
    path = '/todo/{}/mark_done'
    task = await _get_task(auth_test.db, {'done': done})
    _id = task['_id']

    path = path.format(str(_id))

    await auth_test.login()
    response = await client.post(path)
    assert response.status == 200
    task = await _get_task(auth_test.db, {'_id': _id})
    assert task['done']


async def test_delete(auth_test):
    client = auth_test.client
    task = await _get_task(auth_test.db, {})
    _id = task['_id']
    path = '/todo/{}/delete'.format(str(_id))
    await auth_test.login()
    response = await client.post(path)
    assert response.status == 200
    task = await _get_task(auth_test.db, {'_id': _id})
    assert task is None


@pytest.mark.parametrize('task', [
    _generate_task(randint(1, 5))
    for _ in range(10)
])
async def test_create(auth_test, task):
    path = '/todo/create'
    await auth_test.login()
    client = auth_test.client
    title, *rest = task.split(';')
    response = await client.post(path, data={'task': task})
    assert response.status == 200
    todo = await _get_task(auth_test.db, {'title': title})
    assert todo is not None
    max_priority = await _get_max_priority(auth_test.db)
    assert todo['priority'] == max_priority
