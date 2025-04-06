from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.generic import View


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("bill-list")  # Updated redirect target

        return redirect("login")


def logout_view(request):
    logout(request)
    return redirect("login")
