from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
]