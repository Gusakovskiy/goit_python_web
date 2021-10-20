# вижу три возможности повысить производительность:
# - использовать dict вместо списка таплов
# - использовать set для поиска пересечений
# - использовать списковое включение для создания финального списка e-mail


def get_pro_users():
    user_ids = set()
    with open('pro_users.txt', 'r') as _f:
        while _f.readable():
            line = _f.readline()
            if not line:
                break
            _id = line.strip()
            if _id.isdigit():
                user_ids.add(int(_id))
    return user_ids


def get_all_user():
    users = dict()
    with open('all_users.txt', 'r') as _f:
        while _f.readable():
            line = _f.readline()
            if not line:
                break
            _id, email = line.strip().split(',')
            if _id.isdigit():
                users[int(_id)] = email
    return users


def get_pro_users_emails():
    users = get_all_user()
    user_emails = [users[i] for i in set(users) & get_pro_users()]
    return user_emails


def main():
    user_emails = get_pro_users_emails()
    print('Get pro users ', len(user_emails))


if __name__ == '__main__':
    # python -m cProfile -s tottime example_profiling.py
    # utility to watch on user interface
    # python -m vmprof example_profiling.py
    main()
