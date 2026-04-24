from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

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
