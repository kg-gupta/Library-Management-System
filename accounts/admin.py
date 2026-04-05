from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'member_id']
    list_filter = ['role']
    search_fields = ['username', 'email', 'member_id']
    fieldsets = UserAdmin.fieldsets + (
        ('Library Information', {
            'fields': ('role', 'phone', 'address', 'member_id')
        }),
    )
