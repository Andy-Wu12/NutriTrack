from django.http import HttpResponseRedirect
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from django.urls import reverse

from .models import CustomUser
from .forms import SignupForm, LoginForm


# Create your views here.
def signup(request):
    if request.method == 'POST':
        # Create form instance and populate it with data from request
        form = SignupForm(request.POST)
        if form.is_valid():
            # Process data in form.cleaned_data
            uname = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Create User model instance and store it in db
            user = CustomUser.objects.create_user(
                username=uname, email=email, password=password
            )
            # Set sessionid cookie to allow for identifying User in requests
            django_login(request, user)
            # Use redirect to prevent form resubmission
            return HttpResponseRedirect(reverse('logs:index'))

        # Redirect to same page and render error message
        return render(request, 'access/signup.html',
                      {'form': form}, status=400)

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('logs:index'))

    form = SignupForm()
    return render(request, 'access/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        # Create form instance and populate it with data from request
        form = LoginForm(request.POST)
        if form.is_valid():
            # Process data in form.cleaned_data
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Find User instance if it exists and verify password.
            # If invalid, redirect to login form again
            user_set = CustomUser.objects.filter(email=email)
            if user_set.exists():
                user = user_set.get(email=email)
                if check_password(password, user.password):
                    # Set session cookie to identify User in requests
                    django_login(request, user)
                    return HttpResponseRedirect(reverse('logs:index'))

        # Redirect to same page and render error message
        return render(request, 'access/login.html',
                      {'form': form}, status=400)

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('logs:index'))

    form = LoginForm()
    return render(request, 'access/login.html', {'form': form})


def logout(request):
    if request.user.is_authenticated:
        django_logout(request)

    return HttpResponseRedirect(reverse('access:login'))
