from django.shortcuts import redirect
from django.views.generic import ListView, View

from apps.bills.models import Bills
from core.views import LoginRequiredMixinView

class BillListView(LoginRequiredMixinView, ListView):
    model = Bills
    context_object_name = 'bills'
    template_name = "bill_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bills = Bills.objects.filter(user=self.request.user)
        context['bills'] = bills
        return context
        

class DefaultView(View):
    def get(self, request, *args, **kwargs):
        return redirect('announcement-list')