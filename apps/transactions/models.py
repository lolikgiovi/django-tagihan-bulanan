from django.db import models

from apps.bills.models import Bills
from core.models import BaseModel


class Transaction(BaseModel):
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE)
    due_date = models.DateField()
    due_time = models.TimeField()
    is_notified = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateTimeField(blank=True, null=True)
