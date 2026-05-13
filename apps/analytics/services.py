from datetime import timedelta

from django.utils import timezone
from django.db.models import Count, Sum, Q, Avg

from apps.tasks.models import Task
from apps.sessions.models import FocusSession
from apps.users.models import User

from .schemas import ProductivityAnalyticsData, LeaderboardMemberData
from .models import DailyStats


def update_daily_stats(
    user, focus_duration_seconds, interruptions_count, tasks_completed=0
):
    today = timezone.now().date()
    stats, created = DailyStats.objects.get_or_create(user=user, date=today)

    stats.total_focus_time += focus_duration_seconds
    stats.interruptions_count += interruptions_count
    stats.completed_tasks_count += tasks_completed

    # Calculate score: (completed_tasks * 1.0) + (focus_time_hours * 2.0) - (interruptions * 0.5)
    focus_hours = stats.total_focus_time / 3600
    stats.productivity_score = (
        (stats.completed_tasks_count * 1.0)
        + (focus_hours * 2.0)
        - (stats.interruptions_count * 0.5)
    )

    stats.save()
    return stats


class ProductivityAnalyticsService:

    @staticmethod
    def calculate_delta(today: int, yesterday: int) -> int:

        if yesterday == 0:
            return 0

        return round(((today - yesterday) / yesterday) * 100)

    @staticmethod
    def get_productivity_analytics(project=None, user=None, period="day"):
        now = timezone.now()
        today = now.date()

        if period == "day":
            start_date = today
            prev_start_date = today - timedelta(days=1)
        elif period == "week":
            start_date = today - timedelta(days=today.weekday())
            prev_start_date = start_date - timedelta(days=7)
        elif period == "month":
            start_date = today.replace(day=1)
            prev_start_date = (start_date - timedelta(days=1)).replace(day=1)
        else:
            start_date = today
            prev_start_date = today - timedelta(days=1)

        # Filters
        task_filters = Q()
        focus_filters = Q(status=FocusSession.Status.COMPLETED)

        if project:
            task_filters &= Q(project=project)
            focus_filters &= Q(task__project=project)
        elif user:
            # Global analytics for specific user
            task_filters &= Q(assignee=user) | Q(creator=user, project__isnull=True)
            focus_filters &= Q(user=user)

        # Task Stats
        tasks_period = Task.objects.filter(task_filters, created_at__date__gte=start_date)
        completed_tasks_period_qs = Task.objects.filter(
            task_filters, status=Task.Status.DONE, completed_at__date__gte=start_date
        )
        completed_tasks_prev_period_qs = Task.objects.filter(
            task_filters, status=Task.Status.DONE,
            completed_at__date__gte=prev_start_date,
            completed_at__date__lt=start_date
        )

        tasks_created_count = tasks_period.count()
        tasks_completed_count = completed_tasks_period_qs.count()
        tasks_completed_prev_count = completed_tasks_prev_period_qs.count()

        overdue_tasks = Task.objects.filter(
            task_filters,
            deadline__lt=now,
        ).exclude(status=Task.Status.DONE).count()

        completion_rate = 0
        if tasks_created_count > 0:
            completion_rate = round((tasks_completed_count / tasks_created_count) * 100)

        # Focus Stats
        focus_period_qs = FocusSession.objects.filter(
            focus_filters,
            start_time__date__gte=start_date
        )
        focus_prev_period_qs = FocusSession.objects.filter(
            focus_filters,
            start_time__date__gte=prev_start_date,
            start_time__date__lt=start_date
        )

        focus_period_aggregate = focus_period_qs.aggregate(
            total_focus=Sum("duration"),
            avg_focus=Avg("duration"),
        )
        focus_prev_aggregate = focus_prev_period_qs.aggregate(
            total_focus=Sum("duration"),
        )

        focus_period_seconds = focus_period_aggregate["total_focus"] or 0
        focus_prev_seconds = focus_prev_aggregate["total_focus"] or 0
        average_focus_session_seconds = int(focus_period_aggregate["avg_focus"] or 0)

        best_focus_session = focus_period_qs.only("duration").order_by("-duration").first()
        best_focus_duration_seconds = best_focus_session.duration if best_focus_session else 0

        tasks_delta_percent = ProductivityAnalyticsService.calculate_delta(
            tasks_completed_count, tasks_completed_prev_count
        )
        focus_delta_percent = ProductivityAnalyticsService.calculate_delta(
            focus_period_seconds, focus_prev_seconds
        )

        # Members Leaderboard (only for projects)
        leaderboard = []
        top_member_username = None
        top_member_tasks = 0

        if project:
            leaderboard_queryset = (
                completed_tasks_period_qs.filter(assignee__isnull=False)
                .values("assignee__username")
                .annotate(completed_count=Count("id"))
                .order_by("-completed_count")[:5]
            )
            leaderboard = [
                LeaderboardMemberData(
                    username=item["assignee__username"],
                    completed_tasks=item["completed_count"],
                )
                for item in leaderboard_queryset
            ]
            if leaderboard:
                top_member_username = leaderboard[0].username
                top_member_tasks = leaderboard[0].completed_tasks

        active_members_count = focus_period_qs.values("user").distinct().count()

        return ProductivityAnalyticsData(
            tasks_created_today=tasks_created_count,
            tasks_completed_today=tasks_completed_count,
            tasks_completed_yesterday=tasks_completed_prev_count,
            tasks_delta_percent=tasks_delta_percent,
            overdue_tasks=overdue_tasks,
            completion_rate=completion_rate,
            focus_today_seconds=focus_period_seconds,
            focus_yesterday_seconds=focus_prev_seconds,
            focus_delta_percent=focus_delta_percent,
            average_focus_session_seconds=average_focus_session_seconds,
            best_focus_duration_seconds=best_focus_duration_seconds,
            active_members_count=active_members_count,
            top_member_username=top_member_username,
            top_member_tasks=top_member_tasks,
            leaderboard=leaderboard,
        )
