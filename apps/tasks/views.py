from django.db import models
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, Attachment
from .serializers import TaskSerializer, AttachmentSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project', 'status', 'assignee', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'deadline', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        # Return tasks from projects the user has access to
        return Task.objects.filter(
            models.Q(project__owner=user) | models.Q(project__members__user=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save()

class AttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = AttachmentSerializer

    def get_queryset(self):
        user = self.request.user
        return Attachment.objects.filter(
            models.Q(task__project__owner=user) | models.Q(task__project__members__user=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
