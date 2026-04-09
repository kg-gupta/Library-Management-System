from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_FINE = 'fine'
    TYPE_OVERDUE = 'overdue'
    TYPE_DUE_SOON = 'due_soon'
    TYPE_RETURN = 'return'
    TYPE_MANUAL = 'manual'

    TYPE_CHOICES = [
        (TYPE_FINE, 'Fine Notice'),
        (TYPE_OVERDUE, 'Overdue Notice'),
        (TYPE_DUE_SOON, 'Due Soon Reminder'),
        (TYPE_RETURN, 'Return Confirmation'),
        (TYPE_MANUAL, 'Admin Message'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} for {self.user.username}"