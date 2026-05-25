from django.contrib import admin
from .models import User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "is_staff", "streak", "last_activity_at")
    list_filter = ("is_staff", "is_superuser", "is_active", "language")
    search_fields = ("id", "username", "first_name", "last_name")
    readonly_fields = ("created_at", "updated_at", "last_activity_at")