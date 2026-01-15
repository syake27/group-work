from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Method(models.Model):
    method_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    user_icon = models.ImageField(upload_to="user_icons/", null=True, blank=True)
    target_amount = models.IntegerField(default=0)
    is_private = models.BooleanField(default=False)


class SavingRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    method = models.ForeignKey(Method, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    saved_at = models.DateTimeField()
