from module_9.example_tables import users, addresses
from module_9.engine import engine
from faker import Faker
fake = Faker()


def insert_users():
    with engine.connect() as connection:
        for _i in range(5):
            first_name = fake.first_name()
            last_name = fake.last_name()
            insert_user = users.insert().values(
                name=first_name, fullname=f'{first_name} {last_name}'
            ).returning(users.c.id)
            result = connection.execute(insert_user)  # user inserted
            for row in result:
                email = f'{first_name.lower()}.{last_name.lower()}@gmail.com'
                insert_address = addresses.insert().values(
                    user_id=row[0], email_address=email
                )
                a_result = connection.execute(insert_address)  # address inserted
                for a_row in a_result:
                    print(a_row)


if __name__ == '__main__':
    insert_users()