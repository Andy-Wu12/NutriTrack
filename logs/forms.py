from django import forms
from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError

from .models import Food


class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'desc', 'ingredients', 'calories', 'image']
        widgets = {
            'desc': Textarea(),
            'ingredients': Textarea(),
        }

    def clean_calories(self):
        calories = self.cleaned_data['calories']
        if type(calories) != int:
            return ValidationError("Your input is the incorrect type")
        if calories < 0:
            return ValidationError("Must be a number at least 0")

        return calories


class LogSearchForm(forms.Form):
    query = forms.CharField(label='Search logs by food name or creator', required=False)
