from django.db import models

from access.models import CustomUser

# Create your models here.
class Privacy(models.Model):
    user = models.ForeignKey(CustomUser, unique=True, on_delete=models.CASCADE)
    show_logs = models.BooleanField(default=True, verbose_name="Make logs public")

    def __str__(self):
        return f"{self.user.username}'s log privacy settings set to {self.show_logs}"
