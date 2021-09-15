
import click
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from pymongo.database import Database


def check_db():
    db = get_db()
    click.echo(db.test_collection.find())


def get_db():
    """Get database """
    db_name = current_app.config['DB_NAME']
    db_url = f"mongodb://mongo_admin:qwe123@localhost:27017/{db_name}"
    if 'mongo_client' not in g:
        movies_mongo_client = pymongo.MongoClient(db_url)
        g.mongo_client = movies_mongo_client

    if 'db' not in g:
        my_db: Database = getattr(g.mongo_client, db_name)
        g.db = my_db

    return g.db


def close_db(e=None):
    """Closes mongo db  connection"""
    client = g.pop('mongo_client', None)
    _ = g.pop('db', None)
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
    app.cli.add_command(check_db_command)
    app.teardown_appcontext(close_db)