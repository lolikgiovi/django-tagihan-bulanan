from huey.contrib.djhuey import task
from .methods import send_notifications

@task()
def process_notifications():
    send_notifications()