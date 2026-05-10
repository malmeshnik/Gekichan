from rest_framework import serializers
from .models import Project, ProjectMember
from django.contrib.auth import get_user_model

User = get_user_model()
from apps.users.serializers import UserSerializer

class ProjectMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )

    class Meta:
        model = ProjectMember
        fields = ['id', 'user', 'user_id', 'role', 'created_at']

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    members_count = serializers.IntegerField(source='members.count', read_only=True)
    tasks_count = serializers.IntegerField(source='tasks.count', read_only=True)
    overdue_tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'owner',
            'members_count', 'tasks_count', 'overdue_tasks_count',
            'created_at', 'updated_at'
        ]

    def get_overdue_tasks_count(self, obj):
        from apps.tasks.models import Task
        from django.utils import timezone
        return obj.tasks.filter(
            deadline__lt=timezone.now()
        ).exclude(status=Task.Status.DONE).count()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        from apps.tasks.models import Task
        from django.utils import timezone
        from datetime import timedelta
        ret['tasks_in_progress_count'] = instance.tasks.filter(status=Task.Status.IN_PROGRESS).count()
        ret['tasks_done_count'] = instance.tasks.filter(status=Task.Status.DONE).count()
        ret['active_members_count'] = instance.members.filter(user__last_activity_at__gt=timezone.now() - timedelta(minutes=5)).count()
        return ret

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
