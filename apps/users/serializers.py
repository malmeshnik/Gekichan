from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    is_active_now = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'timezone', 'last_activity_at', 'is_active_now']

    def get_is_active_now(self, obj):
        if not obj.last_activity_at:
            return False
        from django.utils import timezone
        from datetime import timedelta
        return obj.last_activity_at > timezone.now() - timedelta(minutes=5)

class TelegramAuthSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField(source='id')

    def create(self, validated_data):
        telegram_id = validated_data.get('id')
        user, created = User.objects.get_or_create(
            id=telegram_id,
            defaults={
                'first_name': f"User_{telegram_id}", # Default first name as required by model
            }
        )
        return user
