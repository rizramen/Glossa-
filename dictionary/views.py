from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Dictionary
from django.views.generic.list import ListView


class DictionaryList(ListView):
    model = Dictionary


class DictionaryHomeView(TemplateView):
    template_name = "dictionary/dictionary_home.html"

class DictionaryDetailView(TemplateView):
    template_name = "dictionary/detail.html"

class AddWordView(TemplateView):
    template_name = "dictionary/add_word.html"

class CreateDictionaryView(CreateView):
    model = Dictionary
    fields = ["name"]
    success_url = reverse_lazy("dictionary:list")
    template_name = "dictionary/create.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Dictionary created successfully")
        return super(CreateDictionaryView, self).form_valid(form)


class DictionaryListView(ListView):

    model = Dictionary

    def get_queryset(self, *args, **kwargs):
        qs = super(DictionaryListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs