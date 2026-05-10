from django.db import models
from rest_framework import serializers
from .models import Task, Attachment
from apps.projects.models import Project
from django.utils import timezone

class AttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.ReadOnlyField(source='uploaded_by.id')

    class Meta:
        model = Attachment
        fields = [
            'id', 'task', 'telegram_file_id', 'file_name',
            'mime_type', 'file_size', 'uploaded_by', 'created_at'
        ]

class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.id')
    attachment_count = serializers.IntegerField(source='attachments.count', read_only=True)
    is_overdue = serializers.SerializerMethodField()
    focus_time_total = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'project', 'creator', 'assignee', 'title',
            'description', 'status', 'priority', 'deadline',
            'attachment_count', 'is_overdue', 'focus_time_total',
            'created_at', 'updated_at'
        ]

    def get_is_overdue(self, obj):
        if obj.deadline and obj.status != Task.Status.DONE:
            return obj.deadline < timezone.now()
        return False

    def get_focus_time_total(self, obj):
        # We'll need to import Session and calculate total time.
        # For now return 0 or implement properly if sessions app is available
        from apps.sessions.models import FocusSession
        sessions = FocusSession.objects.filter(task=obj, end_time__isnull=False)
        total_seconds = sum((s.end_time - s.start_time).total_seconds() for s in sessions)
        return total_seconds

    def validate_project(self, value):
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
