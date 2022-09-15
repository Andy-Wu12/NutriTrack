from django.urls import path
from . import views

# Name space to allow distinction between duplicate views in separate apps
app_name = 'settings'

urlpatterns = [
    path('', views.index, name='index'),
]
