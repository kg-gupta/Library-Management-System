from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    STUDENT = 'student'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (ADMIN, 'Admin'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=STUDENT
    )
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    member_id = models.CharField(max_length=20, unique=True, blank=True, null=True, default=None)

    def is_admin_user(self):
        return self.role == self.ADMIN

    def __str__(self):
        return f"{self.username} ({self.role})"
