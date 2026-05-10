from django.utils import timezone
from .models import DailyStats

def update_daily_stats(user, focus_duration_seconds, interruptions_count, tasks_completed=0):
    today = timezone.now().date()
    stats, created = DailyStats.objects.get_or_create(
        user=user,
        date=today
    )

    stats.total_focus_time += focus_duration_seconds
    stats.interruptions_count += interruptions_count
    stats.completed_tasks_count += tasks_completed

    # Calculate score: (completed_tasks * 1.0) + (focus_time_hours * 2.0) - (interruptions * 0.5)
    focus_hours = stats.total_focus_time / 3600
    stats.productivity_score = (
        (stats.completed_tasks_count * 1.0) +
        (focus_hours * 2.0) -
        (stats.interruptions_count * 0.5)
    )

    stats.save()
    return stats
