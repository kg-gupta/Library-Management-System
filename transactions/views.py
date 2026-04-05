from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, timedelta
from .models import BorrowRecord
from books.models import Book


@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.available_copies < 1:
        messages.error(
            request,
            f'Sorry, no copies of "{book.title}" are currently available.'
        )
        return redirect('books:detail', pk=book_id)

    already_borrowed = BorrowRecord.objects.filter(
        user=request.user,
        book=book,
        status='borrowed'
    ).exists()

    if already_borrowed:
        messages.warning(
            request,
            'You have already borrowed this book.'
        )
        return redirect('books:detail', pk=book_id)

    due = date.today() + timedelta(days=14)

    BorrowRecord.objects.create(
        user=request.user,
        book=book,
        due_date=due
    )

    book.available_copies -= 1
    book.save()

    messages.success(
        request,
        f'You have successfully borrowed "{book.title}". '
        f'Please return it by {due.strftime("%d %B %Y")}.'
    )
    return redirect('transactions:my_books')


@login_required
def return_book(request, record_id):
    record = get_object_or_404(
        BorrowRecord,
        id=record_id,
        user=request.user
    )

    if record.status == 'returned':
        messages.info(request, 'This book has already been returned.')
        return redirect('transactions:my_books')

    record.return_date = date.today()
    record.fine_amount = record.calculate_fine()
    record.status = 'returned'
    record.save()

    record.book.available_copies += 1
    record.book.save()

    if record.fine_amount > 0:
        days_late = (record.return_date - record.due_date).days
        messages.warning(
            request,
            f'"{record.book.title}" returned. You are {days_late} day(s) '
            f'late. Fine: ₹{record.fine_amount:.2f}.'
        )
    else:
        messages.success(
            request,
            f'"{record.book.title}" returned successfully. Thank you!'
        )

    return redirect('transactions:my_books')


@login_required
def my_books(request):
    active_records = BorrowRecord.objects.filter(
        user=request.user
    ).exclude(status='returned').select_related('book')

    history_records = BorrowRecord.objects.filter(
        user=request.user,
        status='returned'
    ).select_related('book')

    for record in active_records:
        if record.is_overdue() and record.status != 'overdue':
            record.status = 'overdue'
            record.save()

    return render(request, 'transactions/my_books.html', {
        'active_records': active_records,
        'history_records': history_records,
    })


@login_required
def all_borrows(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied. Admins only.')
        return redirect('books:list')

    records = BorrowRecord.objects.all().select_related(
        'user', 'book'
    ).order_by('-borrow_date')

    return render(request, 'transactions/all_borrows.html', {
        'records': records
    })