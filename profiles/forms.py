from django import forms


class ProfileForm(forms.Form):
    profile_picture = forms.ImageField(label='Change your profile picture', required=True)


class UserSearchForm(forms.Form):
    username = forms.CharField(label='Search username', required=False)
