from django.db import models
from django.contrib.auth.models import User

class Prediction(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    text       = models.TextField()
    label      = models.CharField(max_length=10)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.label} ({self.confidence}%)"