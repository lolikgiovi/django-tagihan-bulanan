from datetime import date, timedelta

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, ListView, UpdateView,
                                  View)

from apps.bills.models import Bills
from apps.transactions.models import Transaction
from core.views import LoginRequiredMixinView


class BillListView(LoginRequiredMixinView, ListView):
    model = Bills
    context_object_name = "bills"
    template_name = "bill_list.html"

    def get_queryset(self):
        bills = Bills.objects.filter(user=self.request.user).distinct()
        today = timezone.now().date()

        unpaid_bills = []
        paid_bills = []

        for bill in bills:
            next_transaction = (
                Transaction.objects.filter(
                    bill=bill, user=self.request.user, is_paid=False
                )
                .order_by("due_date")
                .first()
            )

            paid_transactions = Transaction.objects.filter(
                bill=bill, user=self.request.user, is_paid=True
            ).order_by(
                "-paid_date"
            )  # desc

            if next_transaction:
                bill_item = {
                    "id": bill.id,
                    "bill_name": bill.bill_name,
                    "bill_amount": bill.bill_amount,
                    "bill_currency": bill.bill_currency,
                    "payment_account": bill.payment_account,
                    "transaction_id": next_transaction.id,
                    "due_date": next_transaction.due_date,
                    "is_paid": False,
                    "paid_date": None,
                }

                days_diff = (next_transaction.due_date - today).days

                if days_diff < 0:
                    bill_item["status"] = f"Overdue by {abs(days_diff)} days"
                    bill_item["status_class"] = "text-red-600"
                elif days_diff == 0:
                    bill_item["status"] = "Due today"
                    bill_item["status_class"] = "text-blue-600 font-medium"
                else:
                    bill_item["status"] = f"Due in {days_diff} days"
                    bill_item["status_class"] = "text-gray-600"

                unpaid_bills.append(bill_item)

            for transaction in paid_transactions:
                paid_bills.append(
                    {
                        "id": bill.id,
                        "bill_name": bill.bill_name,
                        "bill_amount": bill.bill_amount,
                        "bill_currency": bill.bill_currency,
                        "payment_account": bill.payment_account,
                        "transaction_id": transaction.id,
                        "due_date": transaction.due_date,
                        "is_paid": True,
                        "paid_date": transaction.paid_date,
                    }
                )

        unpaid_bills.sort(key=lambda x: x["due_date"])
        return unpaid_bills + paid_bills


class BillPayView(LoginRequiredMixinView, View):
    def post(self, request, pk):
        transaction = get_object_or_404(
            Transaction, pk=pk, user=request.user, is_paid=False
        )
        bill = transaction.bill

        transaction.is_paid = True
        transaction.paid_date = timezone.now()
        transaction.save()
        next_month = transaction.due_date + timedelta(days=30)

        new_transaction = Transaction.objects.create(
            bill=bill,
            user=request.user,
            due_date=date(next_month.year, next_month.month, transaction.due_date.day),
            due_time=transaction.due_time,
            is_notified=False,
            is_paid=False,
        )

        return redirect("bill-list")


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
        response = super().form_valid(form)

        Transaction.objects.create(
            bill=self.object,
            user=self.request.user,
            due_date=form.instance.bill_reminder_date,
            due_time=form.instance.bill_reminder_time,
            is_notified=False,
            is_paid=False,
        )

        return response


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

    def form_valid(self, form):
        response = super().form_valid(form)

        # Update any future transactions for this bill
        future_transactions = Transaction.objects.filter(
            bill=self.object, user=self.request.user, is_paid=False
        )

        if future_transactions.exists():
            for transaction in future_transactions:
                transaction.due_date = form.instance.bill_reminder_date
                transaction.due_time = form.instance.bill_reminder_time
                transaction.save()

        return response


class BillDeleteView(LoginRequiredMixinView, DeleteView):
    model = Bills
    template_name = "bill_confirm_delete.html"
    success_url = reverse_lazy("bill-list")

    def get_queryset(self):
        return Bills.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        bill = self.get_object()
        response = super().delete(request, *args, **kwargs)
        return response
