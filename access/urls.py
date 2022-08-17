from django.urls import path
from . import views

# Name space to allow distinction between duplicate views in separate apps
app_name = 'access'

urlpatterns = [
    path('', views.toSignup, name='home'),
    path('signup', views.signup, name='signup'),
    path('signup/post', views.signup_post, name='signup_post'),
    path('login', views.login, name='login'),
    path('login/post', views.login_post, name='login_post')
]
