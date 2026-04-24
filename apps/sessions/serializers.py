from rest_framework import serializers
from .models import FocusSession

class FocusSessionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = FocusSession
        fields = [
            'id', 'user', 'task', 'start_time', 'end_time',
            'duration', 'interruptions_count', 'context', 'created_at'
        ]
        read_only_fields = ['start_time', 'end_time', 'duration']
