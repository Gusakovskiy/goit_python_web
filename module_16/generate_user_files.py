import faker

_PRO_USERS = 10_000
_ALL_USERS = 100_000
_MAX_ID = 500_000
fake = faker.Faker()


def main():
    users = [(fake.pyint(max_value=_MAX_ID), fake.email()) for _ in range(_ALL_USERS)]
    with open("all_users.txt", "w") as _f:
        _f.writelines([f"{u[0]},{u[1]}\n" for u in users])

    pro_users = [(fake.pyint(max_value=_MAX_ID)) for _ in range(_PRO_USERS)]
    with open("pro_users.txt", "w") as _f:
        _f.writelines([f"{u[0]}\n" for u in pro_users])


if __name__ == "__main__":
    main()
