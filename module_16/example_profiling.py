
def get_pro_users():
    user_ids = []
    with open('pro_users.txt', 'r') as _f:
        while _f.readable():
            line = _f.readline()
            if not line:
                break
            _id = line.strip()
            if _id.isdigit():
                user_ids.append(int(_id))
    return user_ids


def get_all_user():
    users = []
    with open('all_users.txt', 'r') as _f:
        while _f.readable():
            line = _f.readline()
            if not line:
                break
            _id, email = line.strip().split(',')
            if _id.isdigit():
                users.append((int(_id), email))
    return users


def get_pro_users_emails():
    user_emails = []
    users = get_all_user()
    # get only ids
    user_ids = [u[0] for u in users]
    for user_id in get_pro_users():
        if user_id in user_ids:
            _id = user_ids.index(user_id)
            _, email = users[_id]
            user_emails.append(email)
    return user_emails


def main():
    user_emails = get_pro_users_emails()
    print('Get pro users ', len(user_emails))


if __name__ == '__main__':
    # python -m cProfile -s tottime example_profiling.py
    # utility to watch on user interface
    # python -m vmprof example_profiling.py
    main()
