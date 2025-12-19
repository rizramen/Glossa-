from django.urls import path
from django.shortcuts import redirect
from .views import WordOfDayView, AdminSetWordView

urlpatterns = [
    path("", lambda request: redirect("word_of_day")),
    path("admin/word-of-day/", AdminSetWordView.as_view(), name="admin_set_word"),
    path("word-of-day/", WordOfDayView.as_view(), name="word_of_day"),
]
