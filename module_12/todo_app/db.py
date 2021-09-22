import pymongo
from asgiref.sync import sync_to_async
from pymongo.database import Database

from module_12.todo_app.settings import DB_URL


def get_db(app):
    db_name = app["config"]["db_name"]
    db_url = DB_URL.format(db_name)
    if "mongo_client" not in app:
        movies_mongo_client = pymongo.MongoClient(db_url)
        app["mongo_client"] = movies_mongo_client
    if "db" not in app:
        db: Database = getattr(app["mongo_client"], db_name)
        app["db"] = db
    return app["db"]


async def create_db(app):
    return get_db(app)


@sync_to_async
def _close_db(app):
    mongo_client = app.pop("mongo_client", None)
    if mongo_client:
        mongo_client.close()
    app.pop("db", None)


async def close_db(app):
    """Closes mongo db  connection"""
    return await _close_db(app)


def init_app(app):
    app.on_startup.append(create_db)
    app.on_cleanup.append(close_db)
