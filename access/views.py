from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse

min_uname_len = 5
min_pass_len = 8

# Create your views here.
def toSignup(request):
    return HttpResponseRedirect(reverse('access:signup'))


def signup(request):
    return render(request, 'access/signup.html')


def login(request):
    return render(request, 'access/login.html')


def signup_post(request):
    try:
        uname = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
    except KeyError:
        return HttpResponseRedirect(reverse('access:signup'))

    user = User(
        username=uname, email=email, password=make_password(password)
    )
    user.save()

    # TODO: Need to provide session information in the future
    return HttpResponseRedirect(reverse('logs:index'))


def login_post(request):
    try:
        email = request.POST['email']
        password = request.POST['password']
    except KeyError:
        return HttpResponseRedirect(reverse('access:login'))

    return HttpResponse("You have logged in!")
