from django.forms import ModelForm

from access.models import CustomUser


class ProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']
        labels = {
            'profile_picture': "Change your profile picture"
        }
