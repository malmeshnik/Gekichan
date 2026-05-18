from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

from .services import UserStyleService

class UserSerializer(serializers.ModelSerializer):
    style = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'timezone',
            'language', 'avatar_url', 'daily_goal', 'streak', 'style', 'created_at'
        ]

    def get_style(self, obj):
        return UserStyleService.get_user_style(obj)

class TelegramAuthSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    username = serializers.CharField(required=False, allow_null=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False, allow_null=True)
    language_code = serializers.CharField(required=False, allow_null=True)

    def create(self, validated_data):
        telegram_id = validated_data.pop('telegram_id')
        language_code = validated_data.pop('language_code', 'en')

        # Map Telegram language code
        language = 'en'
        if language_code:
            if language_code.startswith('uk') or language_code.startswith('ua'):
                language = 'uk'
            elif language_code.startswith('ru'):
                language = 'ru'

        user, created = User.objects.get_or_create(
            id=telegram_id,
            defaults={
                'first_name': validated_data.get('first_name', f"User_{telegram_id}"),
                'username': validated_data.get('username'),
                'last_name': validated_data.get('last_name'),
                'language': language,
            }
        )
        if not created:
            # Update last interaction or other fields if necessary
            user.last_interaction_at = timezone.now()
            user.save()

        return user
