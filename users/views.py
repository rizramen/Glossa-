from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = "users/login.html"

class RegisterView(TemplateView):
    template_name = "users/register.html"

class AccountView(TemplateView):
    template_name = "users/account.html"
