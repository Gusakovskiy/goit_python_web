print('')
print('CELERY CONFIG')
print('')
task_routes = {
    'tasks.add': 'low-priority',
}
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'add_two_numbers': {
        'task': 'tasks.add',
        'schedule': crontab(hour='*/8', minute=47),
        # solar('sunset', -37.81753, 144.96715),
        'args': (1, 2),
        'options': {
            'expires': 8 * 60 * 60 - 1,
        },
    },
}