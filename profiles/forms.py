from django import forms

from access.models import CustomUser


class ProfileForm(forms.Form):
    profile_picture = forms.ImageField(label='Change your profile picture', required=True)


class UserSearchForm(forms.Form):
    username = forms.CharField(min_length=1)
