from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, Count
from datetime import date
from books.models import Book
from transactions.models import BorrowRecord
from accounts.models import CustomUser


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_admin_user():
            messages.error(request, 'Access denied. Admins only.')
            return redirect('books:list')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@admin_required
def home(request):
    total_books = Book.objects.count()
    total_students = CustomUser.objects.filter(role='student').count()
    active_borrows = BorrowRecord.objects.filter(
        status='borrowed'
    ).count()
    total_returned = BorrowRecord.objects.filter(
        status='returned'
    ).count()

    overdue_records = BorrowRecord.objects.filter(
        status='borrowed',
        due_date__lt=date.today()
    ).select_related('user', 'book')

    total_fines = BorrowRecord.objects.aggregate(
        total=Sum('fine_amount')
    )['total'] or 0

    recent_borrows = BorrowRecord.objects.order_by(
        '-borrow_date'
    )[:10].select_related('user', 'book')

    unavailable_books = Book.objects.filter(available_copies=0)

    context = {
        'total_books': total_books,
        'total_students': total_students,
        'active_borrows': active_borrows,
        'total_returned': total_returned,
        'overdue_records': overdue_records,
        'overdue_count': overdue_records.count(),
        'total_fines': total_fines,
        'recent_borrows': recent_borrows,
        'unavailable_books': unavailable_books,
    }
    return render(request, 'dashboard/home.html', context)