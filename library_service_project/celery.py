from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

from tasks import send_notification


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_service_project.settings')

app = Celery('library_service_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour="12", minute="0"),
        send_notification(),
        name='Check borrowings daily at 12 PM'
    )
