from sqlalchemy import select

from module_9.personal_assistant.db import session
from module_9.personal_assistant.models import User


def user_with_contacts():
    statement = select(
        User
    ).join(
        User.contacts
    )
    result = session.execute(statement).scalars()
    for user in result:
        print(user.first_name, user.last_name)
        for c in user.contacts:
            print(c.email, c.cell_phone)
        print('')


if __name__ == '__main__':
    user_with_contacts()
