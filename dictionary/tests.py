from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Dictionary, Word


class DictionaryAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="password123")
        self.other_user = User.objects.create_user(username="bob", password="password123")
        self.owned_dictionary = Dictionary.objects.create(name="German", language="German", owner=self.user)
        self.foreign_dictionary = Dictionary.objects.create(name="Spanish", language="Spanish", owner=self.other_user)

    def test_dictionary_list_requires_login(self):
        response = self.client.get(reverse("dictionary:list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login/", response.url)

    def test_dictionary_list_only_shows_logged_in_users_dictionaries(self):
        self.client.login(username="alice", password="password123")
        response = self.client.get(reverse("dictionary:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "German")
        self.assertNotContains(response, "Spanish")

    def test_dictionary_detail_blocks_access_to_other_users_dictionary(self):
        self.client.login(username="alice", password="password123")
        response = self.client.get(
            reverse("dictionary:detail", kwargs={"id": self.foreign_dictionary.id})
        )
        self.assertEqual(response.status_code, 404)

    def test_create_dictionary_assigns_logged_in_user_as_owner(self):
        self.client.login(username="alice", password="password123")
        response = self.client.post(reverse("dictionary:create"), {"name": "French", "language": "French"})

        self.assertRedirects(response, reverse("dictionary:list"))
        self.assertTrue(Dictionary.objects.filter(name="French", language="French", owner=self.user).exists())

    def test_create_dictionary_accepts_custom_language(self):
        self.client.login(username="alice", password="password123")
        response = self.client.post(
            reverse("dictionary:create"),
            {
                "name": "Czech Notes",
                "language": "__custom__",
                "custom_language": "Czech",
            },
        )

        self.assertRedirects(response, reverse("dictionary:list"))
        self.assertTrue(Dictionary.objects.filter(name="Czech Notes", language="Czech", owner=self.user).exists())

    def test_add_word_attaches_word_to_owned_dictionary(self):
        self.client.login(username="alice", password="password123")
        response = self.client.post(
            reverse("dictionary:add_word", kwargs={"id": self.owned_dictionary.id}),
            {
                "term": "Haus",
                "definition": "house",
            },
        )

        self.assertRedirects(
            response, reverse("dictionary:detail", kwargs={"id": self.owned_dictionary.id})
        )
        self.assertTrue(
            Word.objects.filter(
                dictionary=self.owned_dictionary,
                term="Haus",
                definition="house",
            ).exists()
        )

    def test_add_word_blocks_access_to_other_users_dictionary(self):
        self.client.login(username="alice", password="password123")
        response = self.client.post(
            reverse("dictionary:add_word", kwargs={"id": self.foreign_dictionary.id}),
            {
                "term": "Casa",
                "definition": "house",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_dictionary_removes_owned_dictionary(self):
        self.client.login(username="alice", password="password123")
        response = self.client.post(
            reverse("dictionary:delete", kwargs={"id": self.owned_dictionary.id})
        )

        self.assertRedirects(response, reverse("dictionary:list"))
        self.assertFalse(Dictionary.objects.filter(id=self.owned_dictionary.id).exists())

    def test_delete_dictionary_blocks_access_to_other_users_dictionary(self):
        self.client.login(username="alice", password="password123")
        response = self.client.post(
            reverse("dictionary:delete", kwargs={"id": self.foreign_dictionary.id})
        )

        self.assertEqual(response.status_code, 404)
