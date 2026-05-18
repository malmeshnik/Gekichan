from rest_framework import serializers
from .models import FocusSession

class FocusSessionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    productivity_score = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = FocusSession
        fields = [
            'id', 'user', 'task', 'status', 'start_time', 'end_time',
            'duration', 'interruptions_count', 'context', 'created_at',
            'last_paused_at', 'total_paused_duration', 'target_duration', 'productivity_score'
        ]
        read_only_fields = ['start_time', 'end_time', 'duration']
