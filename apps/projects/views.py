from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from django.db.models import Q
from .models import Project
from .serializers import ProjectSerializer
from .services import ProjectService

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(owner=user) | Q(members__user=user)
        ).distinct().select_related('owner').prefetch_related('members__user').order_by('-created_at')

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
