from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Count
from rest_framework import viewsets, decorators
from rest_framework.response import Response
from apps.sessions.models import FocusSession
from apps.tasks.models import Task
from .serializers import TodayStatSerializer, DashboardSerializer

class StatsViewSet(viewsets.ViewSet):

    @decorators.action(detail=False, methods=['get'])
    def today(self, request):
        user = request.user
        today = timezone.now().date()

        sessions = FocusSession.objects.filter(
            user=user,
            start_time__date=today
        )
        total_focus_time = sessions.aggregate(Sum('duration'))['duration__sum'] or 0
        interruptions_count = sessions.aggregate(Sum('interruptions_count'))['interruptions_count__sum'] or 0

        completed_tasks_count = Task.objects.filter(
            assignee=user,
            status=Task.Status.DONE,
            updated_at__date=today
        ).count()

        data = {
            'total_focus_time': total_focus_time,
            'completed_tasks_count': completed_tasks_count,
            'interruptions_count': interruptions_count
        }
        serializer = TodayStatSerializer(data)
        return Response(serializer.data)

    @decorators.action(detail=False, methods=['get'])
    def dashboard(self, request):
        user = request.user
        today = timezone.now().date()

        def get_stats_for_range(days):
            start_date = today - timedelta(days=days-1)
            stats = []
            for i in range(days):
                date = start_date + timedelta(days=i)
                focus_time = FocusSession.objects.filter(
                    user=user,
                    start_time__date=date
                ).aggregate(Sum('duration'))['duration__sum'] or 0

                tasks_done = Task.objects.filter(
                    assignee=user,
                    status=Task.Status.DONE,
                    updated_at__date=date
                ).count()

                stats.append({
                    'date': date,
                    'focus_time': focus_time,
                    'tasks_done': tasks_done
                })
            return stats

        data = {
            'last_7_days': get_stats_for_range(7),
            'last_30_days': get_stats_for_range(30)
        }
        serializer = DashboardSerializer(data)
        return Response(serializer.data)
