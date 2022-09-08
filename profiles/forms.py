from django.forms import ModelForm

from access.models import CustomUser


class ProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['image']
