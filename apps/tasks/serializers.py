from django.db import models
from rest_framework import serializers
from .models import Task, TaskAttachment
from apps.projects.models import Project

class TaskAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.ReadOnlyField(source='uploaded_by.id')
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = TaskAttachment
        fields = [
            'id', 'task', 'file', 'file_url', 'telegram_file_id', 'file_name',
            'mime_type', 'file_size', 'uploaded_by', 'created_at'
        ]

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None

class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.id')
    assignee_name = serializers.ReadOnlyField(source='assignee.first_name')
    project_name = serializers.ReadOnlyField(source='project.name')
    attachments = TaskAttachmentSerializer(many=True, read_only=True)
    attachments_count = serializers.IntegerField(source='attachments.count', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'project',
            'project_name',
            'creator',
            'assignee',
            'assignee_name',
            'title',
            'description',
            'status',
            'priority',
            'deadline',
            'attachments',
            'attachments_count',
            'created_at',
            'updated_at'
        ]

    def validate_project(self, value):
        if value is None:
            return value
        user = self.context['request'].user
        # Ensure user has access to the project
        if not Project.objects.filter(id=value.id).filter(
            models.Q(owner=user) | models.Q(members__user=user)
        ).exists():
             raise serializers.ValidationError("You do not have access to this project.")
        return value

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add focus_time (this would typically come from an aggregation)
        # For now, let's just make sure it's in the payload if needed
        # In a real app we'd annotate this in the queryset
        data['focus_time'] = getattr(instance, 'focus_time_seconds', 0)
        return data
