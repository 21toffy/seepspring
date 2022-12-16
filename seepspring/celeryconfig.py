import os
from celery.schedules import crontab
# Celery Config
from seepspring.settings import (
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND
)
broker_url = CELERY_BROKER_URL
result_backend = CELERY_RESULT_BACKEND
task_default_queue = 'seepspring_core'
beat_schedule = {
    # 'terminate_expired_tokens': {
    #     'task': 'terminate_expired_tokens',
    #     # 'schedule': crontab(minute=0, hour=0)
    #     'schedule': 10.0
    # },

    'update_defaulters_new_balance': {
        'task': 'update_defaulters_new_balance',
        # 'schedule': timedelta(seconds=1)#crontab(minute="*/1") #crontab(minute=0, hour=0)
        'schedule': crontab(minute=0, hour=0)


    }
}
timezone = 'Africa/Lagos'
beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
