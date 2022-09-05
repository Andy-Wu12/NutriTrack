from django.shortcuts import HttpResponse, render
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        uid = request.user.id
        users = User.objects.exclude(pk=uid).order_by('username')
    else:
        users = User.objects.all().order_by('username')

    return render(request, 'profiles/index.html', {'users': users})


def user(request, user_id):
    user_obj = User.objects.get(pk=user_id)

    return render(request, 'profiles/user.html', {'user': user_obj})
