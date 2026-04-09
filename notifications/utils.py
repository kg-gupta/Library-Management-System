from .models import Notification


def notify_fine(user, book_title, fine_amount, days_late):
    Notification.objects.create(
        user=user,
        notification_type=Notification.TYPE_FINE,
        title='Fine Notice',
        message=(
            f'You have a fine of ₹{fine_amount:.2f} for returning '
            f'"{book_title}" {days_late} day(s) late. '
            f'Please pay at the library counter.'
        )
    )


def notify_overdue(user, book_title, due_date):
    Notification.objects.create(
        user=user,
        notification_type=Notification.TYPE_OVERDUE,
        title='Overdue Book Notice',
        message=(
            f'Your borrowed book "{book_title}" was due on '
            f'{due_date.strftime("%d %B %Y")}. '
            f'Please return it immediately to avoid additional fines.'
        )
    )


def notify_due_soon(user, book_title, due_date):
    Notification.objects.create(
        user=user,
        notification_type=Notification.TYPE_DUE_SOON,
        title='Book Due Soon',
        message=(
            f'Reminder: "{book_title}" is due on '
            f'{due_date.strftime("%d %B %Y")}. '
            f'Please return it on time to avoid fines.'
        )
    )


def notify_return_confirmed(user, book_title):
    Notification.objects.create(
        user=user,
        notification_type=Notification.TYPE_RETURN,
        title='Return Confirmed',
        message=(
            f'Thank you! Your return of "{book_title}" '
            f'has been confirmed successfully.'
        )
    )


def notify_manual(user, title, message):
    Notification.objects.create(
        user=user,
        notification_type=Notification.TYPE_MANUAL,
        title=title,
        message=message
    )