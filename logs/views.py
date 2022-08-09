from django.http import HttpResponse
from django.template import loader

from .models import Log

def index(request):
    latest_logs = Log.objects.order_by('-pub_date')
    template = loader.get_template('logs/index.html')
    context = {
        'latest_logs': latest_logs
    }
    return HttpResponse(template.render(context, request))


def detail(request, log_id):
    return HttpResponse(f"This is global log #{log_id}")


def comments(request, log_id):
    return HttpResponse(f"You're adding a comment to log #{log_id}")
