import os.path

from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout

from .forms import PasswordForm, EmailForm, DeleteForm
from access.models import CustomUser
from logs.models import Log

# Create your views here.
@login_required
def index(request):
    return render(request, 'settings/index.html')


@login_required
def password(request):
    context = {}

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(pk=request.user.id)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
        else:
            context['form'] = form
            return render(request, 'settings/password.html', context)

        # User needs to login again
        return HttpResponseRedirect(reverse('access:login'))

    context['form'] = PasswordForm()
    return render(request, 'settings/password.html', context)


@login_required
def email(request):
    context = {}

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(pk=request.user.id)
            user.email = form.cleaned_data['email']
            user.save()
        else:
            context['form'] = form
            return render(request, 'settings/email.html', context)

        # Make user login again
        logout(request)
        return HttpResponseRedirect(reverse('access:login'))

    context['form'] = EmailForm()
    return render(request, 'settings/email.html', context)


@login_required
def delete(request):
    context = {}

    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            # Still need to validate correct password
            user = CustomUser.objects.get(pk=request.user.id)
            if user.check_password(form.cleaned_data['password']):
                delete_account_data(user)
                return HttpResponseRedirect(reverse('access:signup'))

        context['error'] = 'Incorrect password!'
        context['form'] = DeleteForm()
        return render(request, 'settings/delete.html', context)

    context['form'] = DeleteForm()
    return render(request, 'settings/delete.html', context)


@login_required
def privacy(request):
    pass


def delete_account_data(user: CustomUser):
    logs = Log.objects.filter(creator=user.id)

    # Delete all log images
    for log in logs:
        img_path = log.food.image.path
        if os.path.exists(img_path):
            os.remove(img_path)

    # Delete profile picture
    pro_pic_path = user.profile_picture.path
    if os.path.exists(pro_pic_path):
        os.remove(pro_pic_path)

    user.delete()
