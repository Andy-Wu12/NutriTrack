from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# Create your views here.
def toSignup(request):
    return HttpResponseRedirect(reverse('access:signup'))


def signup(request):
    return render(request, 'access/signup.html')


def login(request):
    return render(request, 'access/login.html')
