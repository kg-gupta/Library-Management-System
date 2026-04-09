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

    # Mark all as read when page is opened
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

    students = CustomUser.objects.filter(role='student')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        title = request.POST.get('title')
        message_text = request.POST.get('message')

        if user_id == 'all':
            for student in students:
                notify_manual(student, title, message_text)
            messages.success(
                request,
                f'Notification sent to all {students.count()} students.'
            )
        else:
            user = get_object_or_404(CustomUser, id=user_id)
            notify_manual(user, title, message_text)
            messages.success(
                request,
                f'Notification sent to {user.get_full_name() or user.username}.'
            )
        return redirect('dashboard:home')

    return render(request, 'notifications/send_notification.html', {
        'students': students,
    })