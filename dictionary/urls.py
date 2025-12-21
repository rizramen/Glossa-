from django.urls import path
from .views import (
    DictionaryHomeView,
    DictionaryListView,
    DictionaryDetailView,
    CreateDictionaryView,
    AddWordView
)

app_name = "dictionary"


urlpatterns = [
    path('', DictionaryHomeView.as_view(), name='dictionary_home'),
    path("list/", DictionaryListView.as_view(), name="list"),
    path("<int:id>/", DictionaryDetailView.as_view(), name="detail"),
    path("create/", CreateDictionaryView.as_view(), name="create"),
    path("<int:id>/add-word/", AddWordView.as_view(), name="add_word"),
]
