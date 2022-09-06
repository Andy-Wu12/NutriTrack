from django.urls import path
from . import views

# Name space to allow distinction between duplicate views in separate apps
app_name = 'profiles'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/', views.user, name='user')
]
