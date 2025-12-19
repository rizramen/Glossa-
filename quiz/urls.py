from django.urls import path
from .views import QuizStartView, QuizQuestionView, QuizResultView

urlpatterns = [
    path("start/", QuizStartView.as_view(), name="start"),
    path("question/", QuizQuestionView.as_view(), name="question"),
    path("result/", QuizResultView.as_view(), name="result"),
]
