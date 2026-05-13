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
    def get_productivity_analytics(project):

        today = timezone.localdate()
        yesterday = today - timedelta(days=1)

        # Project users
        project_users = (
            User.objects.filter(project_memberships__project=project)
            .only("id", "username")
            .distinct()
        )

        tasks_today = Task.objects.filter(
            project=project,
            created_at__date=today,
        )

        completed_tasks_today_qs = Task.objects.filter(
            project=project,
            status=Task.Status.DONE,
            completed_at__date=today,
        )

        completed_tasks_yesterday_qs = Task.objects.filter(
            project=project,
            status=Task.Status.DONE,
            completed_at__date=yesterday,
        )

        tasks_created_today = tasks_today.count()

        tasks_completed_today = completed_tasks_today_qs.count()

        tasks_completed_yesterday = completed_tasks_yesterday_qs.count()

        overdue_tasks = (
            Task.objects.filter(
                project=project,
                deadline__lt=timezone.now(),
            )
            .exclude(status=Task.Status.DONE)
            .count()
        )

        completion_rate = 0

        if tasks_created_today > 0:
            completion_rate = round((tasks_completed_today / tasks_created_today) * 100)

        focus_today_qs = FocusSession.objects.filter(
            task__project=project,
            status=FocusSession.Status.COMPLETED,
            start_time__date=today,
        )

        focus_yesterday_qs = FocusSession.objects.filter(
            task__project=project,
            status=FocusSession.Status.COMPLETED,
            start_time__date=yesterday,
        )

        focus_today_aggregate = focus_today_qs.aggregate(
            total_focus=Sum("duration"),
            avg_focus=Avg("duration"),
            best_focus=Sum("duration"),
            interruptions=Sum("interruptions_count"),
        )

        focus_yesterday_aggregate = focus_yesterday_qs.aggregate(
            total_focus=Sum("duration"),
        )

        focus_today_seconds = focus_today_aggregate["total_focus"] or 0

        focus_yesterday_seconds = focus_yesterday_aggregate["total_focus"] or 0

        average_focus_session_seconds = int(focus_today_aggregate["avg_focus"] or 0)

        best_focus_session = (
            focus_today_qs.only("duration").order_by("-duration").first()
        )

        best_focus_duration_seconds = (
            best_focus_session.duration if best_focus_session else 0
        )

        tasks_delta_percent = ProductivityAnalyticsService.calculate_delta(
            tasks_completed_today,
            tasks_completed_yesterday,
        )

        focus_delta_percent = ProductivityAnalyticsService.calculate_delta(
            focus_today_seconds,
            focus_yesterday_seconds,
        )

        top_member = (
            completed_tasks_today_qs.filter(assignee__isnull=False)
            .values(
                "assignee__username",
            )
            .annotate(
                completed_count=Count("id"),
            )
            .order_by("-completed_count")
            .first()
        )

        leaderboard_queryset = (
            completed_tasks_today_qs
            .filter(assignee__isnull=False)
            .values(
                "assignee__username",
            )
            .annotate(
                completed_count=Count("id"),
            )
            .order_by("-completed_count")[:3]
        )

        leaderboard = [
            LeaderboardMemberData(
                username=item["assignee__username"],
                completed_tasks=item["completed_count"],
            )
            for item in leaderboard_queryset
        ]

        active_members_count = focus_today_qs.values("user").distinct().count()

        return ProductivityAnalyticsData(
            tasks_created_today=tasks_created_today,
            tasks_completed_today=tasks_completed_today,
            tasks_completed_yesterday=tasks_completed_yesterday,
            tasks_delta_percent=tasks_delta_percent,
            overdue_tasks=overdue_tasks,
            completion_rate=completion_rate,
            focus_today_seconds=focus_today_seconds,
            focus_yesterday_seconds=focus_yesterday_seconds,
            focus_delta_percent=focus_delta_percent,
            average_focus_session_seconds=average_focus_session_seconds,
            best_focus_duration_seconds=best_focus_duration_seconds,
            active_members_count=active_members_count,
            top_member_username=(
                top_member["assignee__username"] if top_member else None
            ),
            top_member_tasks=(top_member["completed_count"] if top_member else 0),
            leaderboard=leaderboard,
        )
