from datetime import timedelta

from django.utils import timezone
from django.db import models

from access.models import CustomUser


class Food(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    desc = models.CharField('description', max_length=1000)
    ingredients = models.CharField(max_length=500)
    calories = models.IntegerField(default=0)
    image = models.ImageField(upload_to='logs', null=True, blank=True,
                              verbose_name='Image (Optional)')

    def __str__(self):
        return f"{self.name} contributed {self.calories} calories."


class Log(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    food = models.OneToOneField(Food, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Date published')

    def __str__(self):
        return f"{self.creator.username} ate {self.food.name} on {self.pub_date.date()}."


class Comment(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('Date commented')

    def __str__(self):
        return f"{self.creator.username} said {self.comment} on {self.pub_date.date()} "

    def is_recent(self):
        now = timezone.now()
        return now - timedelta(days=1) <= self.pub_date <= now
