from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Log, Comment

def index(request):
    latest_logs = Log.objects.order_by('-pub_date')
    context = {
        'latest_logs': latest_logs
    }
    return render(request, 'logs/index.html', context)


def detail(request, log_id):
    log = get_object_or_404(Log, pk=log_id)
    comments = log.comment_set.all()
    context = {
        'log': log,
        'comment_list': comments
    }

    return render(request, 'logs/detail.html', context)


def comment(request, log_id):
    try:
        comment_data = request.POST['comment-text']

    except (KeyError, Comment.DoesNotExist):
        return render(request, 'logs/detail.html', {'log': get_object_or_404(Log, pk=log_id)})
    # Get user currently signed in
        # Placeholder for now is to use admin account
    if len(comment_data.strip()) > 0:
        commenter = User.objects.get(pk=1)
        log = Log.objects.get(pk=log_id)

        new_comment = Comment(creator=commenter, log=log, comment=comment_data,
                              pub_date=timezone.now())

        new_comment.save()
    # Redirect to prevent post data from being reused in case of back button click
    return HttpResponseRedirect(reverse('logs:detail', args=(log_id,)))
