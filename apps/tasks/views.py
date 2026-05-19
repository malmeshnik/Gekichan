from django.db import models
from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import Task, TaskAttachment
from .serializers import TaskSerializer, TaskAttachmentSerializer
from .services import TaskService

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'assignee', 'priority']
    permission_classes = [permissions.IsAuthenticated]

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        from django.utils import timezone
        now = timezone.now()

        period = self.request.query_params.get('period')
        if period == 'today':
            today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            queryset = queryset.filter(deadline__lte=today_end)
        elif period == 'week':
            week_end = now + timezone.timedelta(days=7)
            queryset = queryset.filter(deadline__lte=week_end)
        elif period == 'month':
            month_end = now + timezone.timedelta(days=30)
            queryset = queryset.filter(deadline__lte=month_end)

        project = self.request.query_params.get('project')
        if project == 'null':
            queryset = queryset.filter(project__isnull=True)
        elif project:
            queryset = queryset.filter(project=project)

        deadline_date = self.request.query_params.get('deadline_date')
        if deadline_date:
            queryset = queryset.filter(deadline__date=deadline_date)

        deadline_after = self.request.query_params.get('deadline_after')
        if deadline_after:
            queryset = queryset.filter(deadline__date__gte=deadline_after)

        deadline_before = self.request.query_params.get('deadline_before')
        if deadline_before:
            queryset = queryset.filter(deadline__date__lte=deadline_before)

        overdue = self.request.query_params.get('overdue')
        if overdue == 'true':
            from django.utils import timezone
            queryset = queryset.filter(deadline__lt=timezone.now()).exclude(status=Task.Status.DONE)

        return queryset

    def get_queryset(self):
        user = self.request.user
        from django.utils import timezone
        from apps.projects.models import ProjectMember

        # Base filter: personal tasks or project tasks
        queryset = Task.objects.filter(
            models.Q(project__isnull=True, creator=user) |
            models.Q(project__isnull=True, assignee=user) |
            models.Q(project__owner=user) |
            models.Q(project__members__user=user)
        ).distinct()

        # Role-based restriction for members in projects
        # If user is only a MEMBER in a project, they should only see their own tasks in that project
        # We need a complex filter here.
        # Tasks in projects where user is MEMBER: show only if creator=user or assignee=user
        # Tasks in projects where user is OWNER/ADMIN: show all
        # Personal tasks: show all (already covered by project__isnull=True)

        projects_where_member = ProjectMember.objects.filter(
            user=user, role=ProjectMember.Role.MEMBER
        ).values_list('project_id', flat=True)

        if projects_where_member.exists():
            queryset = queryset.filter(
                ~models.Q(project_id__in=projects_where_member)
                |
                (
                    models.Q(project_id__in=projects_where_member)
                    &
                    (
                        models.Q(creator=user)
                        |
                        models.Q(assignee=user)
                    )
                )
            )

        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        tomorrow_start = today_start + timezone.timedelta(days=1)
        tomorrow_end = today_end + timezone.timedelta(days=1)

        return queryset.annotate(
            focus_time_seconds=models.Sum('focus_sessions__duration'),
            priority_weight=models.Case(
                models.When(priority='high', then=models.Value(3)),
                models.When(priority='medium', then=models.Value(2)),
                models.When(priority='low', then=models.Value(1)),
                default=models.Value(0),
                output_field=models.IntegerField(),
            ),
            is_overdue=models.Case(
                models.When(
                    deadline__lt=now,
                    then=models.Case(
                        models.When(status=Task.Status.DONE, then=models.Value(False)),
                        default=models.Value(True),
                    )
                ),
                default=models.Value(False),
                output_field=models.BooleanField(),
            ),
            is_today=models.Case(
                models.When(
                    deadline__lte=today_end,
                    deadline__gte=today_start,
                    then=models.Value(True)
                ),
                default=models.Value(False),
                output_field=models.BooleanField(),
            ),
            is_tomorrow=models.Case(
                models.When(
                    deadline__lte=tomorrow_end,
                    deadline__gte=tomorrow_start,
                    then=models.Value(True)
                ),
                default=models.Value(False),
                output_field=models.BooleanField(),
            )
        ).select_related('project', 'assignee', 'creator').order_by(
            '-is_overdue', '-is_today', '-is_tomorrow', '-priority_weight', 'deadline', '-created_at'
        )

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if 'status' in request.data and request.data['status'] != instance.status:
            TaskService.update_status(request.user, instance, request.data['status'])
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        TaskService.delete_task(request.user, instance.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskAttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = TaskAttachmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TaskAttachment.objects.filter(
            models.Q(task__project__owner=user) | models.Q(task__project__members__user=user)
        ).distinct().select_related('task', 'uploaded_by')

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
