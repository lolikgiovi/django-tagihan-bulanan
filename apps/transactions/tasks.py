from huey.contrib.djhuey import task, periodic_task
from huey import crontab
from .methods import send_notifications

@task()
def process_notifications():
    send_notifications()

@periodic_task(crontab(minute="*"))
def test_notification_check():
    send_notifications()