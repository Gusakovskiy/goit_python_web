from faker import Faker
from sqlalchemy import MetaData
from sqlalchemy import create_engine

from module_9.settings import CONNECTION_STRING_MODULE_9
from module_9.simple_project.models import user

engine = create_engine(CONNECTION_STRING_MODULE_9)

metadata = MetaData()
fake = Faker()


def main():
    with engine.connect() as connection:
        for _i in range(10):
            first_name = fake.first_name()
            last_name = fake.last_name()
            insert_user = user.insert().values(
                first_name=first_name,
                last_name=last_name,
                address=fake.address(),
                email=f'{first_name.lower()}.{last_name.lower()}@gmail.com'
            )
            _result = connection.execute(insert_user)  # user inserted


if __name__ == '__main__':
    # alembic configuration created with command alembic init alembic

    # create revision from command line
    # alembic revision -m "init"

    # apply revision
    # alembic upgrade head

    # check current revision: alembic current
    # history alembic history --verbose

    # add new collumn
    # alembic revision -m "Add a column phone to user"

    # upgrade
    # alembic upgrade head

    # something wrong with data and we need to downgrade

    # downgrade
    # alembic downgrade -1
    # or with revision number

    # delete everything
    # alembic downgrade base
    # change target_metadata
    # generate revision
    # alembic revision --autogenerate -m "Init revision"
    main()