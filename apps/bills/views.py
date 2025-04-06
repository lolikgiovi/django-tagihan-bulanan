from datetime import date, time

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

from apps.bills.models import Bills
from core.views import LoginRequiredMixinView


class BillListView(LoginRequiredMixinView, ListView):
    model = Bills
    context_object_name = 'bills'
    template_name = "bill_list.html"

    def get_queryset(self):
        bills = Bills.objects.filter(user=self.request.user)
        today = date.today()
        for bill in bills:
            bill.due_days = abs((bill.bill_reminder_date - today).days)
            bill.is_overdue = False
            if bill.bill_reminder_date < today:
                bill.is_overdue = True

        sorted_bills = sorted(bills, key=lambda x: x.due_days)
        return sorted_bills


class BillCreateView(LoginRequiredMixinView, CreateView):
    model = Bills
    template_name = "bill_form.html"
    fields = [
        "bill_name",
        "bill_amount",
        "bill_currency",
        "bill_reminder_date",
        "bill_reminder_time",
        "payment_account",
    ]
    success_url = reverse_lazy("bill-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create"] = True
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BillUpdateView(LoginRequiredMixinView, UpdateView):
    model = Bills
    template_name = "bill_form.html"
    fields = [
        "bill_name",
        "bill_amount",
        "bill_currency",
        "bill_reminder_date",
        "bill_reminder_time",
        "payment_account",
    ]
    success_url = reverse_lazy("bill-list")

    def get_queryset(self):
        return Bills.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create"] = False
        return context


class BillDeleteView(LoginRequiredMixinView, DeleteView):
    model = Bills
    template_name = "bill_confirm_delete.html"
    success_url = reverse_lazy("bill-list")

    def get_queryset(self):
        return Bills.objects.filter(user=self.request.user)
