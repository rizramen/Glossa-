from django.views.generic import TemplateView

class WordOfDayView(TemplateView):
    template_name = "wordofday/word_of_day.html"

class AdminSetWordView(TemplateView):
    template_name = "wordofday/admin_set_word.html"
