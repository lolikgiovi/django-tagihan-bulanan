from django.urls import path

from apps.bills.views import (BillCreateView, BillDeleteView, BillListView,
                              BillPayView, BillUpdateView)

urlpatterns = [
    path("bills/", BillListView.as_view(), name="bill-list"),
    path("bills/create/", BillCreateView.as_view(), name="bill-create"),
    path("bills/<uuid:pk>/edit/", BillUpdateView.as_view(), name="bill-update"),
    path("bills/<uuid:pk>/delete/", BillDeleteView.as_view(), name="bill-delete"),
    path("bills/<uuid:pk>/pay/", BillPayView.as_view(), name="bill-pay"),
]
