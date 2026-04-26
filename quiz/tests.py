from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from dictionary.models import Dictionary, Word

from .models import Quiz


class QuizFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="password123")
        self.other_user = User.objects.create_user(username="bob", password="password123")
        self.dictionary = Dictionary.objects.create(name="German Basics", language="de", owner=self.user)
        self.other_dictionary = Dictionary.objects.create(name="French", language="fr", owner=self.other_user)
        self.word_one = Word.objects.create(dictionary=self.dictionary, term="Haus", definition="house")
        self.word_two = Word.objects.create(dictionary=self.dictionary, term="Baum", definition="tree")
        self.word_three = Word.objects.create(dictionary=self.dictionary, term="Buch", definition="book")

    def test_quiz_home_requires_login(self):
        response = self.client.get(reverse("quiz:quiz_home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_start_quiz_rejects_other_users_dictionary(self):
        self.client.login(username="alice", password="password123")
        response = self.client.post(
            reverse("quiz:start"),
            {"dictionary": self.other_dictionary.id},
        )

        self.assertRedirects(response, reverse("quiz:quiz_home"))
        self.assertFalse(Quiz.objects.filter(dictionary=self.other_dictionary, user=self.user).exists())

    def test_start_quiz_creates_quiz_and_question_page(self):
        self.client.login(username="alice", password="password123")
        response = self.client.post(
            reverse("quiz:start"),
            {"dictionary": self.dictionary.id},
        )

        self.assertRedirects(response, reverse("quiz:question"))
        quiz = Quiz.objects.get(user=self.user, dictionary=self.dictionary)
        session = self.client.session["active_quiz"]
        self.assertEqual(session["quiz_id"], quiz.id)
        self.assertEqual(len(session["word_ids"]), 3)

    def test_quiz_submission_records_result_and_redirects_to_results(self):
        self.client.login(username="alice", password="password123")
        self.client.post(reverse("quiz:start"), {"dictionary": self.dictionary.id})

        while True:
            response = self.client.get(reverse("quiz:question"))
            if response.status_code == 302:
                break

            word = response.context["word"]
            post_response = self.client.post(
                reverse("quiz:question"),
                {"selected_word_id": str(word.id)},
            )
            if post_response.status_code == 302 and post_response.url != reverse("quiz:question"):
                response = post_response
                break

        quiz = Quiz.objects.get(user=self.user, dictionary=self.dictionary)
        self.assertRedirects(response, reverse("quiz:result", kwargs={"quiz_id": quiz.id}))

        result_response = self.client.get(reverse("quiz:result", kwargs={"quiz_id": quiz.id}))
        self.assertEqual(result_response.status_code, 200)
        self.assertContains(result_response, "3 out of 3")
        self.assertEqual(quiz.results.count(), 3)
