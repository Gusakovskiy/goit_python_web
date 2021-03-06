import random

from faker import Faker
from sqlalchemy import exists, and_
from module_9.personal_assistant.db import session, engine
from sqlalchemy.sql.expression import func
from module_9.personal_assistant.models import (
    Contact, Company, User, company_user_table
)

fake = Faker()


def create_user_contacts():
    for _i in range(500):
        first_name = fake.first_name()
        last_name = fake.last_name()
        user = User(
            first_name=first_name,
            last_name=last_name,
            birth_day=fake.date_of_birth(),
        )
        session.add(user)
        should_create_contact = _i % 2 == 0
        if should_create_contact:
            session.commit()
            contact = Contact(
                user_id=user.user_id,
                address=fake.address(),
                email=f'{first_name.lower()}.{last_name.lower()}@gmail.com',
                cell_phone=fake.phone_number()
            )
            session.add(contact)
    session.commit()


def create_company():
    for _i in range(5):
        c = Company(
            name=fake.company(),
            description=fake.bs(),
            domain_name=fake.domain_name(),
            founded=fake.date_this_decade(),
        )
        session.add(c)
    session.commit()


def create_relation_user_companies():
    users = session.query(User).order_by(func.random()).limit(300)
    companies = session.query(Company).all()
    with engine.connect() as connection:
        for user in users:
            company = random.choice(companies)
            insert_relationship = company_user_table.insert().values(
                user_id=user.user_id,
                company_id=company.company_id,
                job_title=fake.job(),
            )
            _result = connection.execute(insert_relationship)  # user inserted


def create_more_contacts():
    users = session.query(User.user_id).order_by(func.random()).limit(300)
    for user in users:
        contact = Contact(
            user_id=user.user_id,
            address=fake.address(),
            email=fake.ascii_free_email(),
            cell_phone=fake.phone_number()
        )
        session.add(contact)
    session.commit()


def create_more_jobs():
    # what wrong ?
    user_ids = session.query(company_user_table.c.user_id).order_by(func.random()).limit(50)
    companies = session.query(Company).all()
    with engine.connect() as connection:
        for user_row in session.execute(user_ids):
            user_id = user_row[0]
            company = random.choice(companies)
            job_exists = session.query(
                exists().where(
                    and_(
                        company_user_table.c.user_id == user_id,
                        company_user_table.c.company_id == company.company_id,
                    )
                )
            ).scalar()
            if job_exists:
                continue
            insert_relationship = company_user_table.insert().values(
                user_id=user_id,
                company_id=company.company_id,
                job_title=fake.job(),
            )
            _result = connection.execute(insert_relationship)


def main():
    create_company()
    create_user_contacts()
    create_relation_user_companies()
    create_more_contacts()
    create_more_jobs()


if __name__ == '__main__':
    main()
