from django.shortcuts import HttpResponse, render

from access.models import CustomUser


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        uid = request.user.id
        users = CustomUser.objects.exclude(pk=uid).order_by('username')
    else:
        users = CustomUser.objects.all().order_by('username')

    return render(request, 'profiles/index.html', {'users': users})


def user(request, user_id):
    user_obj = CustomUser.objects.get(pk=user_id)

    return render(request, 'profiles/user.html', {'target': user_obj})
