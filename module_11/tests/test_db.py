from module_11.personal_app.db import get_db

from pymongo.database import Collection


def test_get_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()


def test_get_users(app):
    with app.app_context():
        db = get_db()
        user_collection: Collection = db.user
        find_all_users = list(user_collection.find())
        assert len(find_all_users) == 4


def test_test_user_exists(app):
    with app.app_context():
        db = get_db()
        user_collection: Collection = db.user
        test_user = user_collection.find_one({'username': 'test'})
        assert test_user
