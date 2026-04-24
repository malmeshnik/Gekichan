from rest_framework import serializers
from .models import Project, ProjectMember

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at', 'updated_at']

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
