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
    def get_productivity_analytics(project=None, user=None, period="day", start_custom=None, end_custom=None, requester=None):
        now = timezone.now()
        today = now.date()

        # Role-based access for project analytics
        is_admin = False
        if project and requester:
            from apps.projects.models import ProjectMember
            is_admin = project.owner == requester or ProjectMember.objects.filter(
                project=project, user=requester, role__in=[ProjectMember.Role.ADMIN, ProjectMember.Role.OWNER]
            ).exists()

        if start_custom and end_custom:
            start_date = start_custom
            end_date = end_custom
            prev_start_date = start_date - (end_date - start_date + timedelta(days=1))
        elif period == "day":
            start_date = today
            end_date = today
            prev_start_date = today - timedelta(days=1)
            # Default to last 8 hours for daily view if it's "now"
            if end_date == today:
                now_time = timezone.now()
                eight_hours_ago = now_time - timedelta(hours=8)
        elif period == "week":
            start_date = today - timedelta(days=today.weekday())
            end_date = today
            prev_start_date = start_date - timedelta(days=7)
        elif period == "month":
            start_date = today.replace(day=1)
            end_date = today
            prev_start_date = (start_date - timedelta(days=1)).replace(day=1)
        elif period == "year":
            start_date = today.replace(month=1, day=1)
            end_date = today
            prev_start_date = start_date.replace(year=start_date.year - 1)
        else:
            start_date = today
            end_date = today
            prev_start_date = today - timedelta(days=1)

        # Filters
        task_filters = Q()
        focus_filters = Q(status=FocusSession.Status.COMPLETED)

        if project:
            task_filters &= Q(project=project)
            focus_filters &= Q(task__project=project)
            if not is_admin and requester:
                # If requester is not admin, show only their data in the project
                task_filters &= Q(assignee=requester)
                focus_filters &= Q(user=requester)
        elif user:
            # Global analytics for specific user
            task_filters &= Q(assignee=user) | Q(creator=user, project__isnull=True)
            focus_filters &= Q(user=user)

        # Task Stats
        tasks_period = Task.objects.filter(
            task_filters, created_at__date__gte=start_date, created_at__date__lte=end_date
        )
        completed_tasks_period_qs = Task.objects.filter(
            task_filters,
            status=Task.Status.DONE,
            completed_at__date__gte=start_date,
            completed_at__date__lte=end_date,
        )
        completed_tasks_prev_period_qs = Task.objects.filter(
            task_filters,
            status=Task.Status.DONE,
            completed_at__date__gte=prev_start_date,
            completed_at__date__lt=start_date,
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
            focus_filters, start_time__date__gte=start_date, start_time__date__lte=end_date
        )
        focus_prev_period_qs = FocusSession.objects.filter(
            focus_filters,
            start_time__date__gte=prev_start_date,
            start_time__date__lt=start_date,
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

        # Members Leaderboard (only for projects - only for admins)
        leaderboard = []
        top_member_username = None
        top_member_tasks = 0

        if project and is_admin:
            leaderboard_queryset = (
                completed_tasks_period_qs.filter(assignee__isnull=False)
                .values("assignee__username", "assignee__first_name")
                .annotate(completed_count=Count("id"))
                .order_by("-completed_count")[:5]
            )
            leaderboard = [
                LeaderboardMemberData(
                    username=item["assignee__username"],
                    first_name=item["assignee__first_name"],
                    completed_tasks=item["completed_count"],
                )
                for item in leaderboard_queryset
            ]
            if leaderboard:
                top_member_username = leaderboard[0].username
                top_member_tasks = leaderboard[0].completed_tasks

        active_members_count = focus_period_qs.values("user").distinct().count()

        # Team member focus stats for admin (only for projects - only for admins)
        member_focus_stats = []
        if project and is_admin:
            member_focus_queryset = (
                focus_period_qs.values("user__username", "user__first_name")
                .annotate(total_duration=Sum("duration"))
                .order_by("-total_duration")
            )
            member_focus_stats = [
                {
                    "username": item["user__username"],
                    "first_name": item["user__first_name"],
                    "total_focus_seconds": item["total_duration"]
                }
                for item in member_focus_queryset
            ]

        # Streaks and Best Day (for global analytics)
        focus_streak = 0
        tasks_streak = 0
        best_day = None
        chart_data = []

        if user:
            # Focus Streak
            focus_dates = (
                FocusSession.objects.filter(user=user, status=FocusSession.Status.COMPLETED)
                .values_list("start_time__date", flat=True)
                .distinct()
                .order_by("-start_time__date")
            )
            current_streak_date = today
            # If nothing today, check if streak was alive yesterday
            if focus_dates and focus_dates[0] != today and focus_dates[0] == today - timedelta(days=1):
                 current_streak_date = today - timedelta(days=1)

            for f_date in focus_dates:
                if f_date == current_streak_date:
                    focus_streak += 1
                    current_streak_date -= timedelta(days=1)
                elif f_date > current_streak_date:
                    continue
                else:
                    break

            # Task Streak (any task completed)
            task_dates = (
                Task.objects.filter(assignee=user, status=Task.Status.DONE)
                .values_list("completed_at__date", flat=True)
                .distinct()
                .order_by("-completed_at__date")
            )
            current_task_streak_date = today
            # If nothing today, check if streak was alive yesterday
            if task_dates and task_dates[0] != today and task_dates[0] == today - timedelta(days=1):
                 current_task_streak_date = today - timedelta(days=1)

            for t_date in task_dates:
                if t_date == current_task_streak_date:
                    tasks_streak += 1
                    current_task_streak_date -= timedelta(days=1)
                elif t_date > current_task_streak_date:
                    continue
                else:
                    break

            # Best Day
            best_day_stat = DailyStats.objects.filter(user=user).order_by("-productivity_score").first()
            if best_day_stat:
                best_day = {
                    "date": best_day_stat.date.isoformat(),
                    "score": float(best_day_stat.productivity_score)
                }

            # Chart Data
            if period == "day":
                # Hourly breakdown for today - showing all 24h but highlight last 8h if requested
                # Requirement: "from now - 8 hours to now with possibility to scroll"
                # We return all 24 hours but the frontend will handle the initial scroll position.
                for h in range(24):
                    hour_focus = focus_period_qs.filter(start_time__hour=h).aggregate(s=Sum("duration"))["s"] or 0
                    hour_tasks = completed_tasks_period_qs.filter(completed_at__hour=h).count()
                    chart_data.append({
                        "label": f"{h:02d}:00",
                        "focus_time": hour_focus,
                        "tasks_completed": hour_tasks,
                        "productivity_score": 0
                    })
            elif period == "week" or (start_custom and end_custom):
                # Daily breakdown (Requirement: show daily if custom range or week)
                # Limit to 90 days to prevent performance issues
                curr = start_date
                limit_date = start_date + timedelta(days=90)
                while curr <= end_date and curr <= limit_date:
                    day_focus = focus_period_qs.filter(start_time__date=curr).aggregate(s=Sum("duration"))["s"] or 0
                    day_tasks = completed_tasks_period_qs.filter(completed_at__date=curr).count()
                    day_score = DailyStats.objects.filter(user=user, date=curr).values_list("productivity_score", flat=True).first() or 0
                    chart_data.append({
                        "label": curr.strftime("%d.%m"),
                        "date": curr.isoformat(),
                        "focus_time": day_focus,
                        "tasks_completed": day_tasks,
                        "productivity_score": float(day_score)
                    })
                    curr += timedelta(days=1)
            elif period == "month":
                # Weekly aggregation for month
                curr = start_date
                while curr <= end_date:
                    week_end = curr + timedelta(days=6)
                    if week_end > end_date:
                        week_end = end_date

                    week_focus = focus_period_qs.filter(start_time__date__gte=curr, start_time__date__lte=week_end).aggregate(s=Sum("duration"))["s"] or 0
                    week_tasks = completed_tasks_period_qs.filter(completed_at__date__gte=curr, completed_at__date__lte=week_end).count()
                    week_score = DailyStats.objects.filter(user=user, date__gte=curr, date__lte=week_end).aggregate(s=Sum("productivity_score"))["s"] or 0

                    chart_data.append({
                        "label": f"{curr.strftime('%d.%m')}-{week_end.strftime('%d.%m')}",
                        "focus_time": week_focus,
                        "tasks_completed": week_tasks,
                        "productivity_score": float(week_score)
                    })
                    curr += timedelta(days=7)
            elif period == "year":
                # Monthly aggregation
                for m in range(1, 13):
                    month_focus = focus_period_qs.filter(start_time__month=m).aggregate(s=Sum("duration"))["s"] or 0
                    month_tasks = completed_tasks_period_qs.filter(completed_at__month=m).count()
                    month_score = DailyStats.objects.filter(user=user, date__month=m, date__year=now.year).aggregate(s=Sum("productivity_score"))["s"] or 0

                    chart_data.append({
                        "label": now.replace(day=1, month=m).strftime("%b"),
                        "focus_time": month_focus,
                        "tasks_completed": month_tasks,
                        "productivity_score": float(month_score)
                    })

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
            focus_streak=focus_streak,
            tasks_streak=tasks_streak,
            best_day=best_day,
            chart_data=chart_data,
            member_focus_stats=member_focus_stats,
        )
