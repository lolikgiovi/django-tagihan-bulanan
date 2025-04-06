from django.urls import path

from apps.bills.views import BillListView

urlpatterns = [
    path('dashboard/', BillListView.as_view(), name='dashboard'),
]