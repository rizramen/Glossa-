from django.db import models
from django.contrib.auth.models import User
from dictionary.models import Dictionary, Word

"""Quiz database model"""
class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz {self.id}"

"""Quiz result database model"""
class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    correct = models.BooleanField()

    def __str__(self):
        return f"{self.word} - {self.correct}"
