from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


""" Extended User Model """
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_language = models.CharField(max_length=2, choices=[("en", "English"), ("de", "German")], null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    telephone_Number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username