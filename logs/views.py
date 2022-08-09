from django.http import HttpResponse
from django.shortcuts import render

from .models import Log

def index(request):
    latest_logs = Log.objects.order_by('-pub_date')
    context = {
        'latest_logs': latest_logs
    }
    return render(request, 'logs/index.html', context)


def detail(request, log_id):
    return HttpResponse(f"This is global log #{log_id}")


def comments(request, log_id):
    return HttpResponse(f"You're adding a comment to log #{log_id}")
