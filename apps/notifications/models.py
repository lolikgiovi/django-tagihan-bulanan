from django.db import models

from apps.bills.models import Bills
from core.models import BaseModel

class Notification(BaseModel):
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE)
    notification_date = models.DateField()
    notification_time = models.TimeField()
    is_notified = models.BooleanField(default=False)
