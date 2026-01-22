from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import LoginView, RegisterView, AccountView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("account/", AccountView.as_view(), name="account"),
    path('logout/', LogoutView.as_view(), name='logout'),
]
