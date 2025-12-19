from django.db import models
from django.contrib.auth.models import User

"""friendship database model"""
class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendships")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    status = models.CharField(max_length=10, choices=[("pending", "Pending"), ("accepted", "Accepted")])

    def __str__(self):
        return f"{self.user} -> {self.friend} ({self.status})"
