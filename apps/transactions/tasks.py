from huey.contrib.djhuey
from .methods import send_notifications

@task()
def process_notifications():
    send_notifications()