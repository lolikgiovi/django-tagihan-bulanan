from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View


class LoginRequiredMixinView(LoginRequiredMixin):
    login_url = "/login/"
    redirect_field_name = "next"

    class Meta:
        abstract = True


class DefaultView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("bill-list")
        else:
            return redirect("login")
