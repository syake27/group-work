from django.db import models


class MoodRecord(models.Model):
    mood = models.CharField(max_length=20)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mood} - {self.created_at}"


# 1
# from django.db import models
# from django.contrib.auth.models import User


# class MoodRecord(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # ユーザーを関連付ける
#     mood = models.CharField(max_length=20)
#     amount = models.IntegerField()  # デフォルトを削除し、必須に
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.mood} - {self.amount}円 - {self.created_at}"