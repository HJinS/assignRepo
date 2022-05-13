from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

app = Celery('djangoProject', broker='amqp://guest:guest@localhost:5672//')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'createNewRoutineResult': {
        "task": "routine_result.tasks.make_results_task",
        'schedule': crontab(),
    },
}
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
