import os

from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.utils import timezone

from access.models import CustomUser, default_avatar
from logs.models import Log
from .forms import ProfileForm, UserSearchForm
from settings.models import Privacy


# Create your views here.
def index(request):
    context = {}

    if request.method == 'POST':
        search_form = UserSearchForm(request.POST)
        if search_form.is_valid():
            username_query = search_form.cleaned_data['username']
            users = CustomUser.objects.filter(username__icontains=username_query)\
                .exclude(username=request.user.username).order_by('username')
            context['users'] = users
            context['form'] = search_form
            return render(request, 'profiles/index.html', context)
        else:
            return HttpResponseRedirect(reverse('profiles:index'))

    if request.user.is_authenticated:
        uid = request.user.id
        users = CustomUser.objects.exclude(pk=uid).order_by('username')
    else:
        users = CustomUser.objects.all().order_by('username')

    context['users'] = users
    context['form'] = UserSearchForm()
    return render(request, 'profiles/index.html', context)


def user(request, user_id):
    context = {}

    try:
        user_obj = CustomUser.objects.get(pk=user_id)
        user_privacy = Privacy.objects.get(user=user_obj)
        user_logs = Log.objects.filter(creator=user_obj.id).order_by('-pub_date')
        context['target'] = user_obj
        if user_privacy.show_logs or request.user.id == user_id:
            context['logs'] = user_logs
        else:
            context['privacyMessage'] = "This user's logs are private!"

        # Calculate statistics
        context['day_age'] = (timezone.now() - user_obj.date_joined).days
        context['calories_count'] = sum(log.food.calories for log in user_logs)

    except CustomUser.DoesNotExist:
        return HttpResponse('User does not exist!', status=404)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            old_pic = user_obj.profile_picture
            new_pic = form.cleaned_data['profile_picture']
            user_obj.profile_picture = new_pic
            user_obj.save()
            if old_pic != default_avatar:
                if os.path.exists(old_pic.path):
                    os.remove(old_pic.path)

        return HttpResponseRedirect(reverse('profiles:user', args=(user_id, )))

    context['form'] = ProfileForm()

    return render(request, 'profiles/user.html', context)
