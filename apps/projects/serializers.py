from rest_framework import serializers
from .models import Project, ProjectMember
from apps.users.serializers import UserSerializer

class ProjectMemberSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['id', 'user', 'user_detail', 'role', 'label', 'created_at']

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    members = ProjectMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'members', 'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['members_count'] = instance.members.count()
        data['tasks_count'] = instance.tasks.count()

        # Let's use simple counts for now and improve in view via annotation
        # overdue_tasks_count will be provided by view annotation or model property
        data['overdue_tasks_count'] = getattr(instance, 'overdue_tasks_count', 0)
        data['active_members_count'] = getattr(instance, 'active_members_count', 0)
        data['in_progress_tasks_count'] = getattr(instance, 'in_progress_tasks_count', 0)
        data['done_tasks_count'] = getattr(instance, 'done_tasks_count', 0)
        data['total_focus_time'] = getattr(instance, 'total_focus_time', 0)
        data['last_activity'] = getattr(instance, 'last_activity', None)

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        project = super().create(validated_data)

        # Also create ProjectMember with role = "owner"
        ProjectMember.objects.create(
            project=project,
            user=user,
            role=ProjectMember.Role.OWNER
        )
        return project
