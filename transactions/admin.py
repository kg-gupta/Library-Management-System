from django.contrib import admin
from django import forms
from django.utils import timezone
from .models import BorrowRecord


class BorrowRecordAdminForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = '__all__'

    def clean_return_date(self):
        return_date = self.cleaned_data.get('return_date')
        if return_date and return_date < timezone.now().date():
            raise forms.ValidationError(
                'Return date cannot be set to a past date.'
            )
        return return_date

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError(
                'Due date cannot be set to a past date.'
            )
        return due_date


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    form = BorrowRecordAdminForm
    list_display = [
        'user', 'book', 'borrow_date',
        'due_date', 'status', 'fine_amount'
    ]
    list_filter = ['status']
    search_fields = ['user__username', 'book__title']
    readonly_fields = ['borrow_date']