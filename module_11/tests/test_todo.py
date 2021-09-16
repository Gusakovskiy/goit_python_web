from random import randint

import pytest
from bson import ObjectId
from faker import Faker
from pymongo.collection import Collection

from module_11.personal_app.db import get_db

_FAKE_TASK_ID = str(ObjectId())
fake = Faker()


def _get_test_user_collection() -> Collection:
    db = get_db()
    user_collection: Collection = db.user
    test_user = user_collection.find_one({'username': 'test'})
    return getattr(db, test_user['todo_collection'])


def _generate_task(join_number):
    result = []
    for _ in range(join_number):
        result.append(fake.text(max_nb_chars=randint(10, 120)))
    return ';'.join(result)


def test_index(app, client, auth_test):
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth_test.login()
    response = client.get('/')

    assert response.status_code == 200
    response_html = response.data
    assert b'Log Out' in response_html


@pytest.mark.parametrize('path', (
        '/create',
        f'/{_FAKE_TASK_ID}/mark_done',
        f'/{_FAKE_TASK_ID}/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


@pytest.mark.parametrize('path', (
        f'/{_FAKE_TASK_ID}/delete',
        f'/{_FAKE_TASK_ID}/mark_done',
        '/asdasdf/mark_done',
        '/asdasdf/delete',
))
def test_exists_required(client, auth_test, path):
    auth_test.login()
    assert client.post(path).status_code == 404


@pytest.mark.parametrize('done', (
        True,
        False,
))
def test_mark_done(app, client, auth_test, done):
    path = '/{}/mark_done'
    _id = None
    with app.app_context():
        todo_collection: Collection = _get_test_user_collection()
        todo = todo_collection.find_one({'done': done})
        _id = todo['_id']
        path = path.format(str(_id))
    auth_test.login()
    response = client.post(path, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        todo_collection: Collection = _get_test_user_collection()
        todo = todo_collection.find_one({'_id': ObjectId(_id)})
        assert todo['done']


def test_delete(app, client, auth_test):
    path = '/{}/delete'
    _id = None
    with app.app_context():
        todo_collection: Collection = _get_test_user_collection()
        todo = todo_collection.find_one()
        _id = todo['_id']
        path = path.format(str(_id))
    auth_test.login()
    response = client.post(path, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        todo_collection: Collection = _get_test_user_collection()
        todo = todo_collection.find_one({'_id': ObjectId(_id)})
        assert todo is None


@pytest.mark.parametrize('task', [
    _generate_task(randint(1, 5))
    for _ in range(10)
])
def test_create(app, client, auth_test, task):
    path = '/create'
    auth_test.login()
    title, *rest = task.split(';')
    response = client.post(path, data={'task': task}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        todo_collection: Collection = _get_test_user_collection()
        todo = todo_collection.find_one({'title': title})
        assert todo is not None
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
        assert todo['priority'] == max_priority['max_priority']
