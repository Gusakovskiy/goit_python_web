
import click
import pymongo
from flask import g
from flask.cli import with_appcontext
from pymongo.database import Database


def check_db():
    db = get_db()
    click.echo(db.test_collection.find())


def get_db():
    """Get database """
    if 'mongo_client' not in g:
        mongo_db_client = "mongodb://mongo_admin:qwe123@localhost:27017/todo_db"
        movies_mongo_client = pymongo.MongoClient(mongo_db_client)
        g.mongo_client = movies_mongo_client

    if 'db' not in g:
        my_db: Database = g.mongo_client.todo_db
        g.db = my_db

    return g.db


def close_db(e=None):
    """Closes mongo db  connection"""
    client = g.pop('mongo_client', None)
    if client is not None:
        client.close()


@click.command('check-db')
@with_appcontext
def check_db_command():
    """Ge."""
    click.echo('Start checking db ')
    check_db()
    click.echo('Finish checking db.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(check_db_command)