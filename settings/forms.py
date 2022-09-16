from django import forms
from django.core.exceptions import ValidationError

from access.models import CustomUser
from access.forms import min_password_len

class PasswordForm(forms.ModelForm):
    password = forms.CharField()
    confirm_password = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ['password']
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }

    def clean_password(self):
        password = self.data['password']
        if len(password) < min_password_len:
            raise ValidationError("Invalid password length")

        return password

    def clean(self):
        password = self.data['password']
        confirmation = self.data['confirm_password']
        if password != confirmation:
            raise ValidationError("Passwords do not match!")


class EmailForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']
