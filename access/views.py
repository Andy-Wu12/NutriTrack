from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse

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
            User.objects.create_user(
                username=uname, email=email, password=password
            )
            # Use redirect to prevent form resubmission
            return HttpResponseRedirect(reverse('logs:index'))

        # Redirect to same page and prevent form resubmission
        return HttpResponseRedirect(reverse('access:signup'))

    form = SignupForm()
    return render(request, 'access/signup.html', {'form': form})


def login(request):
    return render(request, 'access/login.html')
