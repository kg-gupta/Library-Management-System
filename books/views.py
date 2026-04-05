from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book
from .forms import BookForm
from django.core.paginator import Paginator 


def book_list(request):
    books = Book.objects.all()
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    if query:
        books = books.filter(title__icontains=query) | \
                books.filter(author__icontains=query) | \
                books.filter(isbn__icontains=query)
    if category:
        books = books.filter(category=category)

    categories = Book.objects.values_list('category', flat=True).distinct()

    paginator = Paginator(books, 9)   # 9 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'books/book_list.html', {
        'books': page_obj,         # pass page_obj instead of books
        'query': query,
        'selected_category': category,
        'categories': categories,
        'page_obj': page_obj,
    })


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    already_borrowed = False
    if request.user.is_authenticated:
        already_borrowed = request.user.borrow_records.filter(
            book=book, status='borrowed'
        ).exists()
    return render(request, 'books/book_detail.html', {
        'book': book,
        'already_borrowed': already_borrowed,
    })


@login_required
def add_book(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Only admins can add books.')
        return redirect('books:list')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('books:list')
    else:
        form = BookForm()

    return render(request, 'books/book_form.html', {
        'form': form,
        'title': 'Add New Book'
    })


@login_required
def edit_book(request, pk):
    if not request.user.is_admin_user():
        messages.error(request, 'Only admins can edit books.')
        return redirect('books:list')

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{book.title}" updated successfully!')
            return redirect('books:detail', pk=book.pk)
    else:
        form = BookForm(instance=book)

    return render(request, 'books/book_form.html', {
        'form': form,
        'title': f'Edit: {book.title}'
    })


@login_required
def delete_book(request, pk):
    if not request.user.is_admin_user():
        messages.error(request, 'Only admins can delete books.')
        return redirect('books:list')

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'"{title}" has been deleted.')
        return redirect('books:list')

    return render(request, 'books/book_confirm_delete.html', {
        'book': book
    })