import pymongo
from aioshutil import sync_to_async
from pymongo.database import Database


@sync_to_async
def _init_mongo(app):
    db_name = app['config']['db_name']
    db_url = f"mongodb://mongo_admin:qwe123@localhost:27017/{db_name}"
    movies_mongo_client = pymongo.MongoClient(db_url)
    app['mongo_client'] = movies_mongo_client
    app['db']: Database = getattr(app['mongo_client'], db_name)


async def create_db(app):
    return await _init_mongo(app)


@sync_to_async
def _close_db(app):
    mongo_client = app.pop('mongo_client', None)
    if mongo_client:
        mongo_client.close()
    app.pop('db', None)


async def close_db(app):
    """Closes mongo db  connection"""
    return await _close_db(app)


def init_app(app):
    app.on_startup.append(create_db)
    app.on_cleanup.append(close_db)
