from django.db import models
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'status', 'assignee']

    def get_queryset(self):
        user = self.request.user
        # Return tasks from projects the user has access to
        return Task.objects.filter(
            models.Q(project__owner=user) | models.Q(project__members__user=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save()
