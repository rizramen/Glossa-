from django.urls import path
from .views import QuizStartView, QuizQuestionView, QuizResultView, QuizHomeView

app_name = "quiz"

urlpatterns = [
    path("", QuizHomeView.as_view(), name="quiz_home"),
    path("start/", QuizStartView.as_view(), name="start"),
    path("question/", QuizQuestionView.as_view(), name="question"),
    path("result/<int:quiz_id>/", QuizResultView.as_view(), name="result"),
]
