from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from .forms import PasswordForm, EmailForm
from access.models import CustomUser

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
