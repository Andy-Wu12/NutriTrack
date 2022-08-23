from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
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

    def clean(self):
        email = self.data['email']
        password = self.data['password']

        # Only validate if BOTH fields aren't empty
        # This helps to prevent multiple error messages for same issue
        # in login template, specifically the combination of
        # bad_credential_mess and "Field is required" messages
        if len(email) > 0 and len(password) > 0:
            bad_credential_mess = "Incorrect email/password combination"
            email = self.data['email']
            if not User.objects.filter(email=email).exists():
                raise ValidationError(bad_credential_mess)

            stored_user = User.objects.get(email=email)
            if not check_password(password, stored_user.password):
                raise ValidationError(bad_credential_mess)
