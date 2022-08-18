from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=75, min_length=5, required=True)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    password = forms.PasswordInput()
