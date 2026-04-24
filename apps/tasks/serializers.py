from django.db import models
from rest_framework import serializers
from .models import Task
from apps.projects.models import Project

class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.id')

    class Meta:
        model = Task
        fields = [
            'id', 'project', 'creator', 'assignee', 'title',
            'description', 'status', 'deadline', 'created_at', 'updated_at'
        ]

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
