from sqlalchemy import text

from module_9.engine import engine_chinook
import psycopg2

ps_connection = psycopg2.connect(
    host="localhost",
    database="chinook",
    user="postgres",
    password="qwe123",
)
ps_connection.set_session(autocommit=True)


def worst():
    # bad_query = "'; select true; --"
    bad_query = "'; update actor set first_name = 'Penelope' where actor_id = 1 ; select true; --"
    # with engine_chinook.connect() as connection:
    # connection = engine_chinook.raw_connection()
    with ps_connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM actor WHERE first_name = '%s';" % bad_query
        )
        result = cursor.fetchone()
        for _id, row in enumerate(result):
            print(f"[{_id}]; Track {row}")
            print("")


def better():
    bad_query = "'; update actor set first_name = 'P' where actor_id = 1 ; select true; --"
    with engine_chinook.connect() as connection:
        result = connection.execute(
            "SELECT * FROM actor WHERE first_name = '%s';" % bad_query
        )
        for _id, row in enumerate(result):
            print(f"[{_id}]; Track {row}")
            print("")


def best():
    s = text("SELECT * FROM actor WHERE first_name=:name;")
    bad_query = dict(name="'; update actor set first_name = 'P' where actor_id = 1 ; select true; --")
    with engine_chinook.connect() as connection:
        result = connection.execute(s, bad_query)
        for _id, row in enumerate(result):
            print(f"[{_id}]; Track {row}")
            print("")


if __name__ == '__main__':
    """
    Examples inspired by https://realpython.com/prevent-python-sql-injection/
    """
    worst()
    better()
