from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, current_app
from celery.schedules import timedelta

from tasks import send_notification


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_service_project.settings')

app = Celery('library_service_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls send_notification() every 5 seconds
    sender.add_periodic_task(5.0, send_notification.s(), name='Check borrowings every 5 seconds')
