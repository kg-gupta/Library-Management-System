from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification
from .utils import notify_manual
from accounts.models import CustomUser


@login_required
def my_notifications(request):
    notifications = request.user.notifications.all()
    unread_count = notifications.filter(is_read=False).count()
    notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'notifications/my_notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })


@login_required
def send_manual_notification(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('books:list')

    students = CustomUser.objects.filter(
        role__in=['student', 'staff']
    ).order_by('first_name')

    # Pre-select student if coming from student detail page
    preselected_user_id = request.GET.get('user', '')

    if request.method == 'POST':
        user_id = request.POST.get('user_id', '').strip()
        title = request.POST.get('title', '').strip()
        message_text = request.POST.get('message', '').strip()

        if not title or not message_text:
            messages.error(request, 'Title and message cannot be empty.')
            return render(request, 'notifications/send_notification.html', {
                'students': students,
                'preselected_user_id': preselected_user_id,
            })

        if user_id == 'all':
            count = 0
            for student in students:
                notify_manual(student, title, message_text)
                count += 1
            messages.success(
                request,
                f'Notification sent to all {count} students.'
            )
        else:
            # This is the key fix — properly convert to int before lookup
            try:
                uid = int(user_id)
                user = get_object_or_404(CustomUser, id=uid)
                notify_manual(user, title, message_text)
                messages.success(
                    request,
                    f'Notification sent to '
                    f'{user.get_full_name() or user.username}.'
                )
            except (ValueError, TypeError):
                messages.error(request, 'Invalid student selected.')
                return render(
                    request,
                    'notifications/send_notification.html',
                    {'students': students}
                )

        return redirect('dashboard:home')

    return render(request, 'notifications/send_notification.html', {
        'students': students,
        'preselected_user_id': preselected_user_id,
    })