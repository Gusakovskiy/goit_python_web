from module_9.example_tables_orm import Users, Addresses
from module_9.engine import engine
from sqlalchemy.orm import sessionmaker, joinedload
from faker import Faker
fake = Faker()


DBSession = sessionmaker(
    # https://docs.sqlalchemy.org/en/14/orm/session_api.html
    bind=engine,
    # autocommit=True, # Deprecated since version 1.4:
    # autoflush=True
)
session = DBSession()


def insert_users():
    for _i in range(5):
        first_name = fake.first_name()
        last_name = fake.last_name()
        new_user = Users(name=first_name, fullname=f'{first_name} {last_name}')
        session.add(new_user)
        session.commit()
        print(new_user.id, new_user.fullname)
        email = f'{first_name.lower()}.{last_name.lower()}@gmail.com'
        address = Addresses(
            user=new_user, email_address=email
        )
        session.add(address)
        session.commit()

def query_users():
    address = session.query(Addresses).options(joinedload(Addresses.user)).filter_by(
        email_address='jeffrey.harris@gmail.com'
    ).one()
    print(address)
    print(address.id, address.user.fullname)


if __name__ == '__main__':
    query_users()