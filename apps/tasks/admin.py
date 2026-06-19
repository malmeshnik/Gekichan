from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "assignee", "deadline", "created_at")
    list_filter = ("status", "created_at", "deadline")
    search_fields = ("title", "description", "project__name", "assignee__username")
