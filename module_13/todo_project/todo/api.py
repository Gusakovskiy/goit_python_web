from django.contrib.auth.models import User

from .models import Todo


def _example_todos():
    return [
        dict(title='Register in App', done=True, priority=0),
        dict(title='Plan next week', done=False, description='You doing great', priority=1),
        dict(
            title='Sleep more well',
            done=False,
            description='Sleep is very important for your health',
            priority=3,
        ),
        dict(
            title='Buy healthy food', done=False, priority=4),
    ]


def create_default_todo(user: User):
    todos = []
    for todo in _example_todos():
        todo = Todo(**todo, user=user)
        # DO NOT DO SAVE
        # todo.save()
        todos.append(todo)
    Todo.objects.bulk_create(todos)

