from rest_framework import viewsets, filters, permissions
from django.db.models import Q
from .models import Project, ProjectMember
from .serializers import ProjectSerializer, ProjectMemberSerializer
from apps.users.serializers import UserSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        user = self.request.user
        # Return projects where user is owner OR a member
        return Project.objects.filter(
            Q(owner=user) | Q(members__user=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save()

class ProjectMemberViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectMemberSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        return ProjectMember.objects.filter(project_id=project_id)
