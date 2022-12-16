from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seepspring.settings')

app=Celery("seepspring")

app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule={
    'every_12_am':{
        'task':'update_defaulters_new_balance',   
        "schedule": crontab(minute="*/3")
        # 'schedule': crontab(hour=23)
        # 'schedule': crontab(hour=22, minute=19)
    },
}


app.autodiscover_tasks()
