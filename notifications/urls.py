from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.my_notifications, name='list'),
    path('send/', views.send_manual_notification, name='send'),
]