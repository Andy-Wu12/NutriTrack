from django.urls import path
from . import views

# Name space to allow distinction between duplicate views in separate apps
app_name = 'settings'

urlpatterns = [
    path('', views.index, name='index'),
    path('password', views.password, name='password'),
    path('email', views.email, name='email'),
    path('delete', views.delete, name='delete-acc'),
]
