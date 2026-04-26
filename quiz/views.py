import random

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, TemplateView

from dictionary.models import Dictionary, Word

from .forms import QuizAnswerForm, QuizStartForm
from .models import Quiz, QuizResult


QUIZ_SESSION_KEY = "active_quiz"


class QuizHomeView(LoginRequiredMixin, TemplateView):
    template_name = "quiz/quiz_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["start_form"] = QuizStartForm(user=self.request.user)
        context["dictionaries"] = Dictionary.objects.filter(owner=self.request.user).order_by("-id")
        context["recent_quizzes"] = Quiz.objects.filter(user=self.request.user).select_related(
            "dictionary"
        ).order_by("-created_at")[:5]
        return context


class QuizStartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = QuizStartForm(request.POST, user=request.user)
        if not form.is_valid():
            messages.error(request, "Choose one of your dictionaries to start a quiz.")
            return redirect("quiz:quiz_home")

        dictionary = form.cleaned_data["dictionary"]
        word_ids = list(dictionary.words.values_list("id", flat=True))
        if not word_ids:
            messages.error(request, "Add at least one word to this dictionary before starting a quiz.")
            return redirect("quiz:quiz_home")

        random.shuffle(word_ids)
        quiz = Quiz.objects.create(user=request.user, dictionary=dictionary)
        request.session[QUIZ_SESSION_KEY] = {
            "quiz_id": quiz.id,
            "word_ids": word_ids,
            "current_index": 0,
        }
        request.session.modified = True
        return redirect("quiz:question")


class QuizQuestionView(LoginRequiredMixin, TemplateView):
    template_name = "quiz/question.html"

    def dispatch(self, request, *args, **kwargs):
        self.quiz_state = request.session.get(QUIZ_SESSION_KEY)
        if not self.quiz_state:
            messages.info(request, "Start a quiz first.")
            return redirect("quiz:quiz_home")

        self.quiz = get_object_or_404(
            Quiz.objects.select_related("dictionary"),
            id=self.quiz_state["quiz_id"],
            user=request.user,
        )
        self.word_ids = self.quiz_state["word_ids"]
        self.current_index = self.quiz_state["current_index"]

        if self.current_index >= len(self.word_ids):
            request.session.pop(QUIZ_SESSION_KEY, None)
            return redirect("quiz:result", quiz_id=self.quiz.id)

        self.current_word = get_object_or_404(
            Word.objects.select_related("dictionary"),
            id=self.word_ids[self.current_index],
            dictionary=self.quiz.dictionary,
        )
        self.option_words = self._build_option_words()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quiz"] = self.quiz
        context["dictionary"] = self.quiz.dictionary
        context["word"] = self.current_word
        context["question_number"] = self.current_index + 1
        context["total_questions"] = len(self.word_ids)
        context["form"] = QuizAnswerForm(choices=self._option_choices())
        return context

    def post(self, request, *args, **kwargs):
        form = QuizAnswerForm(request.POST, choices=self._option_choices())
        if not form.is_valid():
            context = self.get_context_data()
            context["form"] = form
            return self.render_to_response(context)

        selected_word_id = int(form.cleaned_data["selected_word_id"])
        is_correct = selected_word_id == self.current_word.id
        QuizResult.objects.create(
            quiz=self.quiz,
            word=self.current_word,
            correct=is_correct,
        )

        self.quiz_state["current_index"] = self.current_index + 1
        request.session[QUIZ_SESSION_KEY] = self.quiz_state
        request.session.modified = True

        if self.quiz_state["current_index"] >= len(self.word_ids):
            request.session.pop(QUIZ_SESSION_KEY, None)
            return redirect("quiz:result", quiz_id=self.quiz.id)
        return redirect("quiz:question")

    def _build_option_words(self):
        distractors = list(
            self.quiz.dictionary.words.exclude(id=self.current_word.id).order_by("?")[:3]
        )
        options = [self.current_word, *distractors]
        random.shuffle(options)
        return options

    def _option_choices(self):
        return [(str(word.id), word.definition) for word in self.option_words]


class QuizResultView(LoginRequiredMixin, DetailView):
    model = Quiz
    pk_url_kwarg = "quiz_id"
    context_object_name = "quiz"
    template_name = "quiz/result.html"

    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user).select_related("dictionary")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = list(self.object.results.select_related("word").all())
        correct_answers = sum(1 for result in results if result.correct)
        context["results"] = results
        context["correct_answers"] = correct_answers
        context["total_questions"] = len(results)
        return context
