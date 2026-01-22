from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Dictionary, Word

#Support by ChatGPT for LoginRequiredMixin and general syntax

class DictionaryHomeView(TemplateView):
    template_name = "dictionary/dictionary_home.html"


class DictionaryListView(LoginRequiredMixin, ListView):
    model = Dictionary
    template_name = "dictionary/dictionary_list.html"

    def get_queryset(self):
        #Only show dictionaries owned by the logged-in user
        return Dictionary.objects.filter(owner=self.request.user).order_by("-id")


class DictionaryDetailView(LoginRequiredMixin, DetailView):
    model = Dictionary
    template_name = "dictionary/detail.html"
    pk_url_kwarg = 'id'

    def get_queryset(self):
        #you can only see your own dictionaries
        return Dictionary.objects.filter(owner=self.request.user)


class AddWordView(LoginRequiredMixin, CreateView):
    model = Word
    fields = ['term', 'definition', 'language']
    template_name = "dictionary/add_word.html"

    def get_success_url(self):
        return reverse_lazy('dictionary:detail', kwargs={'id': self.kwargs['id']})

    def form_valid(self, form):
        # get the dictionary to which the word will be added
        # 404 Error if the dictionary does not belong to the logged-in user
        dictionary = get_object_or_404(Dictionary, id=self.kwargs['id'], owner=self.request.user)
        form.instance.dictionary = dictionary
        return super().form_valid(form)


class CreateDictionaryView(LoginRequiredMixin, CreateView):
    model = Dictionary
    fields = ["name"]
    success_url = reverse_lazy("dictionary:list")
    template_name = "dictionary/create.html"

    def form_valid(self, form):
        # new dictionary is owned by the logged-in user
        form.instance.owner = self.request.user
        messages.success(self.request, "Dictionary created successfully")
        return super(CreateDictionaryView, self).form_valid(form)