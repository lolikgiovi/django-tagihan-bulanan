from django.db import models

from core.models import BaseModel


class Bills(BaseModel):
    bill_name = models.CharField(max_length=100)
    bill_amount = models.DecimalField(decimal_places=2, max_digits=12)

    ALLOWED_CURRENCY = [
        ("idr", "IDR"),
        ("usd", "USD"),
    ]
    bill_currency = models.CharField(max_length=3, choices=ALLOWED_CURRENCY)
    bill_reminder_date = models.DateField()
    bill_reminder_time = models.TimeField()
    payment_account = models.CharField(max_length=30)
