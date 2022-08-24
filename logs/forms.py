from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Food


class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'desc', 'ingredients', 'calories']
        widgets = {
            'desc': Textarea(),
            'ingredients': Textarea
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if name == '':
            return ValidationError("Food name is required")
        return name

    def clean_desc(self):
        desc = self.cleaned_data['desc']
        if desc == '':
            return ValidationError("Description is required")

        return desc

    def clean_ingredients(self):
        ingreds = self.cleaned_data['desc']
        if ingreds == '':
            return ValidationError("Ingredients are required")

        return ingreds

    def clean_calories(self):
        calories = self.cleaned_data['calories']
        if type(calories) != int:
            return ValidationError("Your input is the incorrect type")
        if calories < 0:
            return ValidationError("Must be a number at least 0")

        return calories
