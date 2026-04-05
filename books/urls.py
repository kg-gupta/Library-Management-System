from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='list'),
    path('add/', views.add_book, name='add'),
    path('<int:pk>/', views.book_detail, name='detail'),
    path('<int:pk>/edit/', views.edit_book, name='edit'),
    path('<int:pk>/delete/', views.delete_book, name='delete'),
]