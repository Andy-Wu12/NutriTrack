from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

max_username_len = 75
min_username_len = 5
min_password_len = 8

class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=max_username_len,
                               min_length=min_username_len, required=True)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(min_length=min_password_len,
                               widget=forms.PasswordInput(), required=True)

    def clean_username(self):
        uname = self.cleaned_data['username']
        if User.objects.filter(username=uname).exists():
            raise ValidationError("Username already exists")
        return uname

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
