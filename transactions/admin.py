from django.contrib import admin
from .models import BorrowRecord


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'borrow_date', 'due_date', 'status', 'fine_amount']
    list_filter = ['status']
    search_fields = ['user__username', 'book__title']
    readonly_fields = ['borrow_date']