from sqlalchemy.sql import text

from module_9.engine import engine


def main():
    # https://docs.sqlalchemy.org/en/14/core/engines.html
    s = text("SELECT 1;")
    print(engine.driver)
    print(vars(engine))
    # we didn't connect to database yet
    with engine.connect() as connection:  # conn = engine.connect()
        # PEP 248 https://www.python.org/dev/peps/pep-0248/
        # connection = engine.raw_connection()
        result = connection.execute(s)
        print(vars(result))
        print(result)
        for _id, row in enumerate(result):
            print(f"{_id} row {row}")


if __name__ == '__main__':
    main()
