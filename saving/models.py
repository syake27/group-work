from django.db import models


class MoodRecord(models.Model):
    mood = models.CharField(max_length=20)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mood} - {self.created_at}"
