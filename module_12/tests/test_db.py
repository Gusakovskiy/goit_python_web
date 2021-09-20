from module_12.tests.conftest import UserCollectionHelper


async def test_get_db(db, app):
    assert db is app['db']


async def test_get_users(db, user_collection: UserCollectionHelper):
    find_all_users = await user_collection.find_all_users()
    assert len(find_all_users) == 1


async def test_test_user_exists(user_collection: UserCollectionHelper):
    test_user = await user_collection.find_by_name('test')
    assert test_user
