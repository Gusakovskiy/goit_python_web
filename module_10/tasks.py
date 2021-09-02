from celery import Celery

app = Celery(
    'tasks',
    broker='redis://localhost:6379/10',
)


@app.task
def add(x, y):
    result = x + y
    print('Result of add ', result)
    return x + y


@app.task
def hello():
    return 'hello world'


if __name__ == '__main__':
    # celery -A tasks worker --loglevel=debug -settings=celeryconfig
    pass