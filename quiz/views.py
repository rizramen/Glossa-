from django.views.generic import TemplateView

class QuizStartView(TemplateView):
    template_name = "quiz/start.html"

class QuizQuestionView(TemplateView):
    template_name = "quiz/question.html"

class QuizResultView(TemplateView):
    template_name = "quiz/result.html"
