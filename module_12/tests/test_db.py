from pymongo.collection import Collection


async def test_get_db(db, app):
    assert db is app['db']


async def test_get_users(db):
    user_collection: Collection = db.user
    find_all_users = list(user_collection.find())
    assert len(find_all_users) == 4


async def test_test_user_exists(db):
    user_collection: Collection = db.user
    test_user = user_collection.find_one({'username': 'test'})
    assert test_user
