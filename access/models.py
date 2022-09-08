from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    profile_picture = models.ImageField(default='static/images/default-avatar.jpg')
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} joined on {self.date_joined}"
