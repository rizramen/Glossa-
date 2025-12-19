from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("", lambda request: redirect("word_of_day")),
    path("admin/word-of-day/", views.admin_set_word, name="admin_set_word"),
    path("word-of-day/", views.word_of_day, name="word_of_day"),
]
