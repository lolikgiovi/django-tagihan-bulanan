from django.utils import timezone
import time
from datetime import timedelta

from .models import Transaction


def send_notifications():
    print('------- NOTIFICATION CHECK STARTED -------')
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)

    print(f"Today's date: {today}")
    print(f"Tomorrow's date: {tomorrow}")

    all_transactions = Transaction.objects.all()
    print(f"Total transactions in database: {all_transactions.count()}")

    for t in all_transactions:
        print(
            f"- Due: {t.due_date}, Paid: {t.is_paid}, Notified: {t.is_notified}, Bill Name: {t.bill.bill_name}")

    transactions = Transaction.objects.filter(
        is_paid=False,
        is_notified=False,
        due_date__lte=tomorrow
    ).select_related('bill', 'user')

    print(f"\nAfter filtering, found {transactions.count()} bills that need notifications")

    for transaction in transactions:
        bill_name = transaction.bill.bill_name
        print(f"\nProcessing notification for {bill_name}")
        print(f"Transaction due date: {transaction.due_date}")

        if transaction.due_date == tomorrow:
            status = "due tomorrow"
        elif transaction.due_date == today:
            status = "due today"
        else:
            days_overdue = (today - transaction.due_date).days
            status = f"overdue by {days_overdue} days"

        currency_symbol = '$' if transaction.bill.bill_currency == 'usd' else 'Rp'

        print(f"Bill: {bill_name}")
        print(f"Amount: {currency_symbol}{transaction.bill.bill_amount}")
        print(f"Status: {status}")
        print(f"User: {transaction.user.username}")

        time.sleep(2)

        transaction.is_notified = True
        transaction.save()

        print(f"Notification sent for {bill_name}")
        print("------------------")

    print('------- NOTIFICATION CHECK COMPLETED -------')