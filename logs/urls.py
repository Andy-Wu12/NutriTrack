from django.urls import path
from . import views

# Name space to allow distinction between duplicate views in separate apps
app_name = 'logs'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:log_id>/', views.detail, name='detail'),
    path('<int:log_id>/comment', views.comment, name='add-comment')
]
