from django.contrib import admin
from .models import FocusSession

@admin.register(FocusSession)
class FocusSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "task", "start_time", "duration", "context")
    list_filter = ("context", "start_time")
    search_fields = ("user__username", "task__title")
