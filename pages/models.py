from django.db import models
from dictionary.models import Word

"""word of the Day database model"""
class WordOfTheDay(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    language = models.CharField(max_length=10)
    already_used = models.BooleanField(default=False)

    def __str__(self):
        return self.word.term
