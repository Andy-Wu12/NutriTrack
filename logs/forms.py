from django import forms
from django.forms import ModelForm, Textarea

from .models import Food


class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'desc', 'ingredients', 'image']
        widgets = {
            'desc': Textarea(),
            'ingredients': Textarea({"placeholder": "chicken,string beans,white rice"}),
        }
        labels = {
            'ingredients': f'Enter a list of ingredients that were part'
                           f' of your meal, separated by commas.'
        }

class LogSearchForm(forms.Form):
    query = forms.CharField(label='Search logs by food name or creator', required=False)
