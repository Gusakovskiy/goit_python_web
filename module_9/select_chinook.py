from sqlalchemy import text

from module_9.engine import engine_chinook


def main():
    s = text("SELECT * FROM track WHERE genre_id=:genre_id")
    with engine_chinook.connect() as connection:
        result = connection.execute(s, dict(genre_id=3))
        for _id, row in enumerate(result):
            print(f"[{_id}]; Track {row}")
            print("")


if __name__ == '__main__':
    main()
