from celery import Celery

REDIS_URL = 'redis://localhost:6379/{}'
app = Celery(
    'proj',
    broker=REDIS_URL.format(9),
    backend=REDIS_URL.format(10),
    include=['proj.tasks'],
)
app.conf.update(
    result_expires=3600,
)
app.config_from_object('proj.celeryconfig')
app.autodiscover_tasks()


if __name__ == '__main__':
    # celery --app=proj.celery_app.app worker -l DEBUG
    # celery --app=proj.celery_app.app beat -l DEBUG
    print('START APp')
    app.start()
