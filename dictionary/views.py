
from django.views.generic import TemplateView

class DictionaryHomeView(TemplateView):
    template_name = "dictionary/dictionary_home.html"

class DictionaryListView(TemplateView):
    template_name = "dictionary/list.html"

class DictionaryDetailView(TemplateView):
    template_name = "dictionary/detail.html"

class CreateDictionaryView(TemplateView):
    template_name = "dictionary/create.html"

class AddWordView(TemplateView):
    template_name = "dictionary/add_word.html"
