from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import Log, Comment


# Should list all logs globally like some sort of home page feed
def index(request):
    latest_logs = Log.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    context = {
        'latest_logs': latest_logs
    }
    return render(request, 'logs/index.html', context)


def detail(request, log_id):
    log = get_object_or_404(Log, pk=log_id)
    comments = log.comment_set.filter(pub_date__lte=timezone.now())
    context = {
        'log': log,
        'comment_list': comments
    }

    return render(request, 'logs/detail.html', context)


def create_log(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('access:signup'))

    return render(request, 'logs/create-log.html', {})


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
