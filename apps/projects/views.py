from rest_framework import viewsets
from django.db.models import Q
from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        # Return projects where user is owner OR a member
        return Project.objects.filter(
            Q(owner=user) | Q(members__user=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save()
