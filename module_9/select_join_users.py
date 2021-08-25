from sqlalchemy import select, join

from module_9.example_tables import users, addresses
from module_9.engine import engine


def select_users():
    with engine.connect() as connection:
        query = select(
            users.c.name,
            users.c.fullname,
            addresses.c.email_address,
        ).where(
            users.c.id == 3
        ).select_from(
            users.join(addresses)
        )
        print(query)
        result = connection.execute(query)
        for row in result:
            print(row)


if __name__ == '__main__':
    select_users()
