from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Log

def index(request):
    latest_logs = Log.objects.order_by('-pub_date')
    context = {
        'latest_logs': latest_logs
    }
    return render(request, 'logs/index.html', context)


def detail(request, log_id):
    log = get_object_or_404(Log, pk=log_id)
    context = {
        'log': log
    }

    return render(request, 'logs/detail.html', context)

def comments(request, log_id):
    return HttpResponse(f"You're adding a comment to log #{log_id}")
