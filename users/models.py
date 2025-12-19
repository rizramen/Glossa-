from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


""" Extended User Model """

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE);
    preferred_lang = models.CharField(max_length=2);
    language_chocies = models.CharField(max_length=2);
    age = models.IntegerField;
    telephone_Number = models.CharField(max_length=10);

