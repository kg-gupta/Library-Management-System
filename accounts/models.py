from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message='Phone number must be exactly 10 digits.'
)


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
    phone = models.CharField(
    max_length=10,
    blank=True,
    validators=[phone_validator]
)
    address = models.TextField(blank=True)
    member_id = models.CharField(max_length=20, unique=True, blank=True, null=True, default=None)

    def is_admin_user(self):
        return self.role == self.ADMIN

    def __str__(self):
        return f"{self.username} ({self.role})"
