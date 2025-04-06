from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, ListView, UpdateView,
                                  View)

from apps.bills.models import Bills
from apps.transactions.models import Transaction
from core.views import LoginRequiredMixinView

from .utils import adjust_payment_day, calculate_next_payment_date


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
            ).order_by("-paid_date")

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
                    bill_item["status"] = f"Lewat {abs(days_diff)} hari :("
                    bill_item["status_class"] = "text-red-600"
                elif days_diff == 0:
                    bill_item["status"] = "Ayoo bayar hari inii!"
                    bill_item["status_class"] = "text-blue-600 font-medium"
                else:
                    bill_item["status"] = f"Bayarnya masih {days_diff} hari lagi"
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

        unpaid_bills.sort(key=lambda x: x["due_date"])  # due date asc
        paid_bills.sort(key=lambda x: x["paid_date"], reverse=True)  # paid date desc
        return unpaid_bills + paid_bills


class BillCreateView(LoginRequiredMixinView, CreateView):
    model = Bills
    template_name = "bill_form.html"
    fields = ["bill_name", "bill_amount", "bill_currency", "payment_account"]
    success_url = reverse_lazy("bill-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create"] = True
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        payment_day = int(self.request.POST.get("payment_day", 1))
        due_date = calculate_next_payment_date(payment_day)

        Transaction.objects.create(
            bill=self.object, user=self.request.user, due_date=due_date, is_paid=False
        )

        return response


class BillUpdateView(LoginRequiredMixinView, UpdateView):
    model = Bills
    template_name = "bill_form.html"
    fields = ["bill_name", "bill_amount", "bill_currency", "payment_account"]
    success_url = reverse_lazy("bill-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create"] = False

        next_transaction = (
            Transaction.objects.filter(
                bill=self.object, user=self.request.user, is_paid=False
            )
            .order_by("due_date")
            .first()
        )

        if next_transaction:
            context["payment_day"] = next_transaction.due_date.day

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        payment_day = int(self.request.POST.get("payment_day", 1))

        next_transaction = (
            Transaction.objects.filter(
                bill=self.object, user=self.request.user, is_paid=False
            )
            .order_by("due_date")
            .first()
        )

        if next_transaction:
            current_due_date = next_transaction.due_date
            new_due_date = adjust_payment_day(
                current_due_date.year, current_due_date.month, payment_day
            )

            next_transaction.due_date = new_due_date
            next_transaction.save()

        return response

    def get_queryset(self):
        return Bills.objects.filter(user=self.request.user)


class BillPayView(LoginRequiredMixinView, View):
    def post(self, request, transaction_id):
        transaction = get_object_or_404(
            Transaction, id=transaction_id, user=request.user, is_paid=False
        )

        transaction.is_paid = True
        transaction.paid_date = timezone.now()
        transaction.save()

        bill = transaction.bill
        payment_day = transaction.due_date.day

        if transaction.due_date.month == 12:
            next_month = 1
            next_year = transaction.due_date.year + 1
        else:
            next_month = transaction.due_date.month + 1
            next_year = transaction.due_date.year

        next_due_date = adjust_payment_day(next_year, next_month, payment_day)

        Transaction.objects.create(
            bill=bill, user=request.user, due_date=next_due_date, is_paid=False
        )

        return redirect("bill-list")


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
