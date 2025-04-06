from huey.contrib.djhuey import task, periodic_task
from huey import crontab
from .methods import send_notifications

# scheduler
@periodic_task(crontab(hour=0, minute=5))
def daily_notification_check():
    send_notifications()

# manual
@task()
def process_notifications():
    send_notifications()