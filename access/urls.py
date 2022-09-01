from django.urls import path
from . import views

# Name space to allow distinction between duplicate views in separate apps
app_name = 'access'

urlpatterns = [
    path('', views.signup, name='home'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout')
]
