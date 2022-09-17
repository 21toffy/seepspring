from datetime import timedelta
import os
from celery.schedules import crontab
# Celery Config
# broker_url = os.getenv('CELERY_BROKER_URL')
# result_backend = os.getenv('CELERY_RESULT_BACKEND')


# CELERY_IMPORTS = ("tasks", )
# CELERY_RESULT_BACKEND = "amqp"
# BROKER_URL = "amqp://guest:guest@localhost:5672//"
# CELERY_TASK_RESULT_EXPIRES = 300


# task_default_queue = 'seepspring_core'

beat_schedule = {
    # 'update_defaulters_new_balance': {
    #     'task': 'update_defaulters_new_balance',
    #     'schedule': timedelta(seconds=1)#crontab(minute="*/1") #crontab(minute=0, hour=0)

    # }
}
timezone = 'Africa/Lagos'
beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
