from django.contrib import admin
from .models import DailyStats

@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "total_focus_time", "completed_tasks_count", "productivity_score")
    list_filter = ("date",)
    search_fields = ("user__username", "user__first_name")
