from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow'),
    path('return/<int:record_id>/', views.return_book, name='return'),
    path('my-books/', views.my_books, name='my_books'),
    path('all/', views.all_borrows, name='all_borrows'),
    path('renew/<int:record_id>/', views.renew_borrow, name='renew'),
]