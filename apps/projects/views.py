from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from django.db.models import Q, Count, Sum, Max, OuterRef, Subquery, Case, When, Value, IntegerField, F
from django.utils import timezone
from .models import Project
from .serializers import ProjectSerializer
from .services import ProjectService

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        now = timezone.now()
        five_minutes_ago = now - timezone.timedelta(minutes=5)

        # Build subquery for last activity
        # This is a bit simplified, but captures major events
        # In a real app we might have an ActivityLog model

        qs = Project.objects.filter(
            Q(owner=user) | Q(members__user=user)
        ).distinct().select_related('owner').prefetch_related('members__user')

        qs = qs.annotate(
            active_members_count=Count(
                'members',
                filter=Q(members__user__last_activity_at__gte=five_minutes_ago),
                distinct=True
            ),
            in_progress_tasks_count=Count(
                'tasks',
                filter=Q(tasks__status='in_progress'),
                distinct=True
            ),
            done_tasks_count=Count(
                'tasks',
                filter=Q(tasks__status='done'),
                distinct=True
            ),
            overdue_tasks_count=Count(
                'tasks',
                filter=Q(tasks__status__in=['todo', 'in_progress'], tasks__deadline__lt=now),
                distinct=True
            ),
            total_focus_time=Sum('tasks__sessions__duration_seconds'),
            # Approximate last activity as max of various timestamps
            last_activity=Max('tasks__updated_at') # Simplified
        ).order_by('-created_at')

        return qs

    def perform_create(self, serializer):
        # The serializer.save() would work but service handles ProjectMember
        project = ProjectService.create_project(
            owner=self.request.user,
            name=serializer.validated_data['name'],
            description=serializer.validated_data.get('description')
        )
        # Ensure serializer data is updated with the created project
        serializer.instance = project

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        ProjectService.delete_project(request.user, instance.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @decorators.action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        username = request.data.get('username')
        user_id = request.data.get('user_id')

        if username:
            member, created = ProjectService.add_member_by_username(request.user, pk, username)
        elif user_id:
            member, created = ProjectService.add_member_by_id(request.user, pk, user_id)
        else:
            return Response({"error": "Username or user_id required"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "Member added"}, status=status.HTTP_200_OK)
