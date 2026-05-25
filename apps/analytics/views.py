from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Count

from rest_framework import viewsets, decorators
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.sessions.models import FocusSession
from apps.tasks.models import Task
from apps.projects.models import Project
from apps.analytics.services import ProductivityAnalyticsService

from .serializers import TodayStatSerializer, DashboardSerializer


class StatsViewSet(viewsets.ViewSet):

    def _activate_timezone(self, user):
        import pytz
        if user and hasattr(user, 'timezone') and user.timezone:
            try:
                timezone.activate(pytz.timezone(user.timezone))
            except Exception:
                timezone.deactivate()
        else:
            timezone.deactivate()

    @decorators.action(detail=False, methods=["get"])
    def today(self, request):
        user = request.user
        self._activate_timezone(user)
        today = timezone.localtime(timezone.now()).date()

        sessions = FocusSession.objects.filter(user=user, start_time__date=today)
        total_focus_time = sessions.aggregate(Sum("duration"))["duration__sum"] or 0
        interruptions_count = (
            sessions.aggregate(Sum("interruptions_count"))["interruptions_count__sum"]
            or 0
        )

        completed_tasks_count = Task.objects.filter(
            assignee=user, status=Task.Status.DONE, updated_at__date=today
        ).count()

        data = {
            "total_focus_time": total_focus_time,
            "completed_tasks_count": completed_tasks_count,
            "interruptions_count": interruptions_count,
        }
        serializer = TodayStatSerializer(data)
        return Response(serializer.data)

    @decorators.action(detail=False, methods=["get"])
    def dashboard(self, request):
        user = request.user
        self._activate_timezone(user)
        today = timezone.localtime(timezone.now()).date()

        def get_stats_for_range(days):
            start_date = today - timedelta(days=days - 1)
            stats = []
            for i in range(days):
                date = start_date + timedelta(days=i)
                focus_time = (
                    FocusSession.objects.filter(
                        user=user, start_time__date=date
                    ).aggregate(Sum("duration"))["duration__sum"]
                    or 0
                )

                tasks_done = Task.objects.filter(
                    assignee=user, status=Task.Status.DONE, updated_at__date=date
                ).count()

                stats.append(
                    {"date": date, "focus_time": focus_time, "tasks_done": tasks_done}
                )
            return stats

        data = {
            "last_7_days": get_stats_for_range(7),
            "last_30_days": get_stats_for_range(30),
        }
        serializer = DashboardSerializer(data)
        return Response(serializer.data)


from datetime import date

class ProductivityAnalyticsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id=None):
        period = request.query_params.get("period", "day")
        start_str = request.query_params.get("start")
        end_str = request.query_params.get("end")

        start_custom = None
        end_custom = None

        if start_str and end_str:
            try:
                start_custom = date.fromisoformat(start_str)
                end_custom = date.fromisoformat(end_str)
            except ValueError:
                pass

        user = request.user
        project = None

        if project_id:
            project = Project.objects.get(id=project_id)
            stats = ProductivityAnalyticsService.get_productivity_analytics(
                project=project, period=period, start_custom=start_custom, end_custom=end_custom, requester=user
            )
        else:
            stats = ProductivityAnalyticsService.get_productivity_analytics(
                user=user, period=period, start_custom=start_custom, end_custom=end_custom
            )

        return Response(
            {
                "tasks_created_today": stats.tasks_created_today,
                "tasks_completed_today": stats.tasks_completed_today,
                "tasks_completed_yesterday": stats.tasks_completed_yesterday,
                "tasks_delta_percent": stats.tasks_delta_percent,
                "overdue_tasks": stats.overdue_tasks,
                "completion_rate": stats.completion_rate,
                "focus_today_seconds": stats.focus_today_seconds,
                "focus_yesterday_seconds": stats.focus_yesterday_seconds,
                "focus_delta_percent": stats.focus_delta_percent,
                "average_focus_session_seconds": stats.average_focus_session_seconds,
                "best_focus_duration_seconds": stats.best_focus_duration_seconds,
                "active_members_count": stats.active_members_count,
                "top_member_username": stats.top_member_username,
                "top_member_tasks": stats.top_member_tasks,
                "leaderboard": [
                    {
                        "username": member.username,
                        "first_name": member.first_name,
                        "completed_tasks": member.completed_tasks,
                    }
                    for member in stats.leaderboard
                ],
                "focus_streak": stats.focus_streak,
                "task_streak": stats.tasks_streak,
                "best_day": stats.best_day,
                "chart_data": stats.chart_data,
                "member_focus_stats": stats.member_focus_stats,
                "ai_insight": stats.ai_insight,
            }
        )
