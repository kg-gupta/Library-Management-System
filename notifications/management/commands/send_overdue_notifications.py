from django.core.management.base import BaseCommand
from transactions.models import BorrowRecord
from notifications.utils import notify_overdue
from datetime import date


class Command(BaseCommand):
    help = 'Sends overdue notifications to all students with overdue books'

    def handle(self, *args, **kwargs):
        overdue = BorrowRecord.objects.filter(
            status='borrowed',
            due_date__lt=date.today()
        ).select_related('user', 'book')

        count = 0
        for record in overdue:
            record.status = 'overdue'
            record.save()
            notify_overdue(record.user, record.book.title, record.due_date)
            count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Sent overdue notifications to {count} student(s).'
            )
        )