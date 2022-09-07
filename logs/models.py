from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone


class Food(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField('description', max_length=1000)
    ingredients = models.CharField(max_length=500)
    calories = models.IntegerField(default=0)
    image = models.ImageField(upload_to='', null=True, blank=True)

    def __str__(self):
        return f"{self.name} contributed {self.calories} calories."


class Log(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.OneToOneField(Food, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Date published')

    def __str__(self):
        return f"{self.creator.username} ate {self.food.name} on {self.pub_date.date()}."


class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('Date commented')

    def __str__(self):
        return f"{self.creator} said {self.comment} on {self.pub_date.date()} "

    def is_recent(self):
        now = timezone.now()
        return now - timedelta(days=1) <= self.pub_date <= now
