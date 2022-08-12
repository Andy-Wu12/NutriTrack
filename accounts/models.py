from django.db import models


# Create your models here.
class Account(models.Model):
    email = models.EmailField(unique=True, max_length=75)
    username = models.CharField(unique=True, max_length=25)
    # Bcrypt generates 60 character hashes
    password = models.CharField(max_length=60)

    def __str__(self):
        return f"User {self.username} has email {self.email}"
