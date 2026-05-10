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
    filterset_fields = ['project', 'status', 'assignee', 'priority']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            models.Q(project__owner=user) | models.Q(project__members__user=user)
        ).distinct().annotate(
            focus_time_seconds=models.Sum('sessions__duration_seconds')
        ).select_related('project', 'assignee', 'creator').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if 'status' in request.data and request.data['status'] != instance.status:
            TaskService.update_status(request.user, instance.id, request.data['status'])

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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TaskAttachment.objects.filter(
            models.Q(task__project__owner=user) | models.Q(task__project__members__user=user)
        ).distinct().select_related('task', 'uploaded_by')

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
