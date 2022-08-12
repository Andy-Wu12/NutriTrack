from django.db import models
from django.contrib.auth.models import User

# Custom User model
# from accounts.models import Account


# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField('description', max_length=1000)
    ingredients = models.CharField(max_length=500)
    calories = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} contributed {self.calories} calories."


class Log(models.Model):
    user_acc = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.OneToOneField(Food, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Date published')

    def __str__(self):
        return f"{self.user_acc.username} ate {self.food.name} on {self.pub_date.date()}."
