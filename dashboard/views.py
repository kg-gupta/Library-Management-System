from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, Q
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

    # All students with their borrow stats and total fines
    students = CustomUser.objects.filter(role='student').annotate(
        total_borrows=Count('borrow_records'),
        active_borrows=Count(
            'borrow_records',
            filter=Q(borrow_records__status='borrowed')
        ),
        total_fines=Sum('borrow_records__fine_amount')
    ).order_by('first_name')

    import json
    from datetime import timedelta
    last_7 = [date.today() - timedelta(days=i) for i in range(6, -1, -1)]
    chart_labels = json.dumps([d.strftime('%d %b') for d in last_7])
    chart_data = json.dumps([
        BorrowRecord.objects.filter(borrow_date=d).count()
        for d in last_7
    ])

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
        'students': students,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'dashboard/home.html', context)


@admin_required
def student_detail(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id, role='student')
    borrow_records = BorrowRecord.objects.filter(
        user=student
    ).select_related('book').order_by('-borrow_date')
    total_fine = borrow_records.aggregate(
        total=Sum('fine_amount')
    )['total'] or 0

    return render(request, 'dashboard/student_detail.html', {
        'student': student,
        'borrow_records': borrow_records,
        'total_fine': total_fine,
    })