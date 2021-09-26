from django.contrib.auth.models import User


def create_user(username: str, email: str, password: str) -> User:
    user = User(
        username=username,
        email=email,
        # default False field
        is_staff=False,
        is_superuser=False,
    )
    user.set_password(password)
    user.save()
    return user
