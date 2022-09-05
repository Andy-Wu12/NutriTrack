from django.shortcuts import HttpResponse, render

# Create your views here.
def index(request):
    return HttpResponse("list of users goes here")


def user(request, user_id):
    return HttpResponse("specific user profile here")
