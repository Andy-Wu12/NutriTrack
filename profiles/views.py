from django.shortcuts import HttpResponse, render
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    users = {}
    if request.user.is_authenticated:
        uid = request.user.id
        users = User.objects.exclude(pk=uid)

    else:
        users = User.objects.all()
    return render(request, 'profiles/index.html', {'users': users})


def user(request, user_id):
    return HttpResponse("specific user profile here")
