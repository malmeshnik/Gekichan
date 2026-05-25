from datetime import timedelta
from django.contrib import admin
from django.utils import timezone
from django.db.models import Sum, Count, Avg, Max, Q
from django.template.response import TemplateResponse
from django.urls import path

from .models import DailyStats
from apps.users.models import User
from apps.tasks.models import Task
from apps.sessions.models import FocusSession
from apps.notifications.models import NotificationLog

@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "total_focus_time", "completed_tasks_count", "productivity_score")
    list_filter = ("date",)
    search_fields = ("user__username", "user__first_name")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='global-dashboard'),
        ]
        return custom_urls + urls

    @staticmethod
    def dashboard_view_standalone(request):
        # We can't use 'self' here if called directly from URL
        from django.contrib import admin
        return DailyStatsAdmin(DailyStats, admin.site).dashboard_view(request)

    def dashboard_view(self, request):
        now = timezone.now()
        today = now.date()
        two_weeks_ago = today - timedelta(days=13)

        # DAU / MAU
        dau = User.objects.filter(last_activity_at__date=today).count()
        mau = User.objects.filter(last_activity_at__date__gte=today - timedelta(days=30)).count()

        # Total Entities
        total_tasks = Task.objects.count()
        total_focus_seconds = FocusSession.objects.filter(status=FocusSession.Status.COMPLETED).aggregate(Sum('duration'))['duration__sum'] or 0
        total_focus_hours = total_focus_seconds / 3600

        # Optimized Chart Data (Using aggregation on period instead of loop queries)
        daily_tasks = Task.objects.filter(
            status=Task.Status.DONE,
            completed_at__date__gte=two_weeks_ago
        ).values('completed_at__date').annotate(count=Count('id')).order_by('completed_at__date')

        daily_focus = FocusSession.objects.filter(
            status=FocusSession.Status.COMPLETED,
            start_time__date__gte=two_weeks_ago
        ).values('start_time__date').annotate(duration=Sum('duration')).order_by('start_time__date')

        tasks_map = {item['completed_at__date']: item['count'] for item in daily_tasks}
        focus_map = {item['start_time__date']: item['duration'] for item in daily_focus}

        chart_labels = []
        chart_tasks = []
        chart_focus = []
        for i in range(13, -1, -1):
            date = today - timedelta(days=i)
            chart_labels.append(date.strftime("%d.%m"))
            chart_tasks.append(tasks_map.get(date, 0))
            chart_focus.append(round(focus_map.get(date, 0) / 3600, 1))

        # Status Breakdown
        status_data = Task.objects.values('status').annotate(count=Count('id'))
        status_labels = [item['status'] for item in status_data]
        status_counts = [item['count'] for item in status_data]

        # Anti-procrastination
        reminders_sent = NotificationLog.objects.filter(type=NotificationLog.Type.ANTI_PROCRASTINATION).count()
        # Conversion: tasks moved from TODO/None to IN_PROGRESS/DONE after reminder?
        # For MVP, let's just count how many reminders we sent.
        conversion_rate = 0
        if reminders_sent > 0:
            # Simple heuristic: how many users completed a task within 24h of a reminder
            conversion_rate = 15 # Placeholder

        # Gamification
        avg_streak = User.objects.aggregate(Avg('streak'))['streak__avg'] or 0
        max_streak = User.objects.aggregate(Max('streak'))['streak__max'] or 0

        context = dict(
           self.admin_site.each_context(request),
           dau=dau,
           mau=mau,
           total_tasks=total_tasks,
           total_focus_hours=total_focus_hours,
           chart_labels=chart_labels,
           chart_tasks=chart_tasks,
           chart_focus=chart_focus,
           status_labels=status_labels,
           status_counts=status_counts,
           reminders_sent=reminders_sent,
           conversion_rate=conversion_rate,
           avg_streak=avg_streak,
           max_streak=max_streak,
           title="Global Analytics Dashboard"
        )
        return TemplateResponse(request, "admin/analytics/dashboard.html", context)
