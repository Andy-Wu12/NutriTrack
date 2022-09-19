from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import Food, Log, Comment
from .forms import FoodForm
from settings.models import Privacy


# Should list all logs globally like some sort of home page feed
# Taking into account user privacy settings
def index(request):
    public_log_filter = Privacy.objects.filter(show_logs=True).values_list('id')
    latest_logs = Log.objects.filter(
        pub_date__lte=timezone.now(), creator__in=public_log_filter).order_by('-pub_date')
    context = {
        'latest_logs': latest_logs
    }
    return render(request, 'logs/index.html', context)


def detail(request, log_id):
    context = {}

    log = get_object_or_404(Log, pk=log_id)
    log_privacy = Privacy.objects.get(user=log.creator.id)
    comments = log.comment_set.filter(pub_date__lte=timezone.now())

    if not log_privacy.show_logs and request.user.id != log.creator.id:
        context['privacyMessage'] = 'You do not have permission to view this log!'
    else:
        context['log'] = log
        context['comment_list'] = comments

    if request.method == 'POST':
        # One to one in log means log depends on food.
        # Deleting food will cascade log, but not vice versa
        log.food.delete()
        return HttpResponseRedirect(reverse('logs:index'))

    return render(request, 'logs/detail.html', context)


def create_log(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('access:signup'))

    if request.method == 'POST':
        # Create form instance and populate it with data from request
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            # Process data in form.cleaned_data
            food_name = form.cleaned_data['name']
            desc = form.cleaned_data['desc']
            ingreds = form.cleaned_data['ingredients']
            calories = form.cleaned_data['calories']
            img = form.cleaned_data.get('image')

            food_obj = Food(creator=request.user, name=food_name, desc=desc,
                            ingredients=ingreds, calories=calories, image=img)
            food_obj.save()

            log = Log(creator=request.user, food=food_obj, pub_date=timezone.now())
            log.save()
            return HttpResponseRedirect(reverse('logs:index'))

        # Redirect to same page and render error message
        return render(request, 'logs/create-log.html',
                      {'form': form}, status=400)

    form = FoodForm()

    return render(request, 'logs/create-log.html', {'form': form})


def comment(request, log_id):
    if not request.method == 'POST':
        return HttpResponseRedirect(reverse('logs:detail', args=(log_id,)))

    log = get_object_or_404(Log, pk=log_id)

    try:
        comment_data = request.POST['comment-text']
    except (KeyError, Comment.DoesNotExist):
        error_message = 'Error getting comment data. Please try again!'
        return render(request, 'logs/detail.html', {'log': log,
                                                    'comment_list': log.comment_set.all(),
                                                    'error_message': error_message})
    # Get user currently signed in
    if len(comment_data.strip()) > 0:
        # request.user exists due to session cookie
        # created after login/signup
        commenter = request.user
        log = Log.objects.get(pk=log_id)

        new_comment = Comment(creator=commenter, log=log, comment=comment_data,
                              pub_date=timezone.now())

        new_comment.save()
    # Redirect to prevent post data from being reused in case of back button click
    return HttpResponseRedirect(reverse('logs:detail', args=(log_id,)))
