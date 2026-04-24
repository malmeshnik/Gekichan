from rest_framework import serializers

class DailyStatSerializer(serializers.Serializer):
    date = serializers.DateField()
    focus_time = serializers.IntegerField()
    tasks_done = serializers.IntegerField()

class DashboardSerializer(serializers.Serializer):
    last_7_days = DailyStatSerializer(many=True)
    last_30_days = DailyStatSerializer(many=True)

class TodayStatSerializer(serializers.Serializer):
    total_focus_time = serializers.IntegerField()
    completed_tasks_count = serializers.IntegerField()
    interruptions_count = serializers.IntegerField()
