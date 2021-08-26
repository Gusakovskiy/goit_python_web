from sqlalchemy import select, func, desc, nullslast
from datetime import datetime

from sqlalchemy.orm import joinedload

from module_9.personal_assistant.db import session
from module_9.personal_assistant.models import User, Company, Contact, company_user_table
from sqlalchemy import or_, and_


def user_with_contacts():
    # https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html
    statement = session.query(User).options(joinedload('contacts'))

    result = session.execute(statement).scalars()
    for user in result:
        print(user.full_name)
        for c in user.contacts:
            print(c.email, c.cell_phone)
        print('')


def contact_with_birthday():
    statement = select(
        User
    ).filter(
        or_(
            and_(
                User.birth_day > datetime(year=2017, month=3, day=1),
                User.birth_day < datetime(year=2018, month=1, day=1)
            ),
            User.birth_day > datetime(year=2020, month=12, day=1)
        )
    )
    users = session.execute(statement).scalars()
    for user in users:
        print(f'User {user.full_name} has birthday {user.birth_day}')


def most_working_person():
    statement = session.query(
        User.user_id,
        func.count(Company.company_id).label('number_of_companies')
    ).join(
        User.companies
    ).group_by(
        User.user_id,
    ).order_by(
        desc('number_of_companies')
    ).limit(5).subquery()

    full_query = session.query(
        User, statement.c.number_of_companies
    ).join(
        statement,
        User.user_id == statement.c.user_id
    ).order_by(
        nullslast(desc(statement.c.number_of_companies))
    )
    users = session.execute(full_query)
    for user, number_companies in users:
        print(user.full_name, number_companies)


if __name__ == '__main__':
    user_with_contacts()
    # contact_with_birthday()
    # most_working_person()

