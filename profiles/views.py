import os

from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from access.models import CustomUser
from .forms import ProfileForm

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        uid = request.user.id
        users = CustomUser.objects.exclude(pk=uid).order_by('username')
    else:
        users = CustomUser.objects.all().order_by('username')

    return render(request, 'profiles/index.html', {'users': users})


def user(request, user_id):
    user_obj = CustomUser.objects.get(pk=user_id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            old_pic = user_obj.profile_picture
            new_pic = form.cleaned_data['profile_picture']
            user_obj.profile_picture = new_pic
            user_obj.save()
            os.remove(old_pic.path)

        return HttpResponseRedirect(reverse('profiles:user', args=(user_id, )))

    return render(request, 'profiles/user.html',
                  {'target': user_obj, 'form': ProfileForm()})
