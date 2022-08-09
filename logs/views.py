from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render

from .models import Log

def index(request):
    latest_logs = Log.objects.order_by('-pub_date')
    context = {
        'latest_logs': latest_logs
    }
    return render(request, 'logs/index.html', context)


def detail(request, log_id):
    context = {}
    try:
        log = Log.objects.get(pk=log_id)
        context['log'] = log
    except Log.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'logs/detail.html', context)

def comments(request, log_id):
    return HttpResponse(f"You're adding a comment to log #{log_id}")
