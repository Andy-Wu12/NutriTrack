from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

default_avatar = "/default/default-avatar.jpg"


# Create your models here.
class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='avatars', default=default_avatar)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} joined on {self.date_joined}"
