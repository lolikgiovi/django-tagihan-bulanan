from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages

from apps.bills.models import Bills
from core.views import LoginRequiredMixinView


class BillListView(LoginRequiredMixinView, ListView):
    model = Bills
    context_object_name = 'bills'
    template_name = "bill_list.html"

    def get_queryset(self):
        return Bills.objects.filter(user=self.request.user)


class BillCreateView(LoginRequiredMixinView, CreateView):
    model = Bills
    template_name = "bill_form.html"
    fields = ['bill_name', 'bill_amount', 'bill_currency', 'bill_reminder_date', 'bill_reminder_time',
              'payment_account']
    success_url = reverse_lazy('bill-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BillUpdateView(LoginRequiredMixinView, UpdateView):
    model = Bills
    template_name = "bill_form.html"
    fields = ['bill_name', 'bill_amount', 'bill_currency', 'bill_reminder_date', 'bill_reminder_time',
              'payment_account']
    success_url = reverse_lazy('bill-list')

    def get_queryset(self):
        return Bills.objects.filter(user=self.request.user)


class BillDeleteView(LoginRequiredMixinView, DeleteView):
    model = Bills
    template_name = "bill_confirm_delete.html"
    success_url = reverse_lazy('bill-list')

    def get_queryset(self):
        return Bills.objects.filter(user=self.request.user)