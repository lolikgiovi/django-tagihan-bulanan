from django.utils import timezone
import time

from .models import Transaction

def send_notifications():
    print('Sending notifications')
    transactions = Transaction.objects.filter(due_date__exact=timezone.now())
    for transaction in transactions:
        print("Sending notification for transaction {}".format(transaction))

        time.sleep(10)

        transaction.is_notified = True
        transaction.save()

        print("Notification sent.")
        print("------------------")