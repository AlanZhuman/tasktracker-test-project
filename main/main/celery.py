import os
from celery import Celery
import time
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main', broker='redis://localhost:6379/0')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    timezone='Asia/Almaty', 
    enable_utc=True, # Храним время в UTC

)

app.autodiscover_tasks(['notifications'])

app.conf.beat_schedule = {
    "celery_expirity_check": {
        "task": 'notifications.tasks.celery_expirity_check',
        "schedule": timedelta(minutes=10),
    },
}