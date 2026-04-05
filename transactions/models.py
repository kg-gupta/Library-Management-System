from django.db import models
from django.conf import settings
from books.models import Book
from datetime import date


class BorrowRecord(models.Model):
    STATUS_BORROWED = 'borrowed'
    STATUS_RETURNED = 'returned'
    STATUS_OVERDUE = 'overdue'
    STATUS_CHOICES = [
        (STATUS_BORROWED, 'Borrowed'),
        (STATUS_RETURNED, 'Returned'),
        (STATUS_OVERDUE, 'Overdue'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='borrow_records'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='borrow_records'
    )
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_BORROWED
    )
    fine_amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00
    )

    def calculate_fine(self):
        today = self.return_date or date.today()
        if today > self.due_date:
            overdue_days = (today - self.due_date).days
            return overdue_days * 2.00
        return 0.00

    def is_overdue(self):
        return date.today() > self.due_date and self.status == self.STATUS_BORROWED

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"

    class Meta:
        ordering = ['-borrow_date']