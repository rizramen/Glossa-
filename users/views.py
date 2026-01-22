from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

# Login Logic created with support from ChatGPT - Created in order to identify User and redirect to dictionary list after login

# Login-Logic
class LoginView(DjangoLoginView):
    template_name = "users/login.html"
    # If login is successful, redirect to the dictionary list
    next_page = reverse_lazy('dictionary:list')

# Registration-Logic
class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = UserCreationForm  # Nutzt das fertige Django-Formular
    success_url = reverse_lazy('login') # Nach der Registrierung zum Login

# Account-View
class AccountView(TemplateView):
    template_name = "users/account.html"