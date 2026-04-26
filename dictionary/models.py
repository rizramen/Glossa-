from django.db import models
from django.contrib.auth.models import User


"""dictionary database model"""
class Dictionary(models.Model):
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dictionaries")

    def __str__(self):
        return self.name

    def get_language_display(self):
        return self.language

"""word database model"""
class Word(models.Model):
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE, related_name="words")
    term = models.CharField(max_length=100)
    definition = models.TextField()

    def __str__(self):
        return self.term
