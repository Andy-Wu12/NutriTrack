from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse

from .forms import SignupForm, LoginForm


# Create your views here.
def signup(request):
    # TODO: Need some way to prevent going back to signup page
    #  once logged in, or automatically redirect back to logs
    if request.method == 'POST':
        # Create form instance and populate it with data from request
        form = SignupForm(request.POST)
        if form.is_valid():
            # Process data in form.cleaned_data
            uname = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            User.objects.create_user(
                username=uname, email=email, password=password
            )
            return HttpResponseRedirect(reverse('logs:index'))
    else:
        form = SignupForm()

    return render(request, 'access/signup.html', {'form': form})


def login(request):
    return render(request, 'access/login.html')
