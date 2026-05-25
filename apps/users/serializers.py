import logging

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

from .services import UserStyleService

logger = logging.getLogger("__name__")

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

from django.conf import settings
from .telegram_auth import validate_telegram_data

class TelegramAuthSerializer(serializers.Serializer):
    init_data = serializers.CharField(required=False, allow_blank=True)
    telegram_id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=False, allow_null=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False, allow_null=True)
    language_code = serializers.CharField(required=False, allow_null=True)

    def validate(self, attrs):
        init_data = attrs.get('init_data')
        logger.info(f"Received init_data: {init_data!r}")

        if init_data:
            user_data = validate_telegram_data(init_data)
            if user_data:
                # Overwrite telegram_id from verified data
                attrs['telegram_id'] = user_data.get('id')
                attrs['first_name'] = user_data.get('first_name')
                attrs['last_name'] = user_data.get('last_name')
                attrs['username'] = user_data.get('username')
                attrs['language_code'] = user_data.get('language_code')
            else:
                raise serializers.ValidationError("Invalid Telegram init data")

        if not settings.DEBUG and not init_data:
            raise serializers.ValidationError("Telegram init data is required")

        if not attrs.get('telegram_id'):
             raise serializers.ValidationError("telegram_id is required")

        return attrs

    def create(self, validated_data):
        telegram_id = validated_data.get('telegram_id')
        language_code = validated_data.get('language_code', 'en')

        # Map Telegram language code
        language = 'en'
        if language_code:
            if language_code.startswith('uk') or language_code.startswith('ua'):
                language = 'uk'
            elif language_code.startswith('ru'):
                language = 'ru'

        defaults = {
            'first_name': validated_data.get('first_name', f"User_{telegram_id}"),
            'username': validated_data.get('username'),
            'last_name': validated_data.get('last_name'),
            'language': language,
        }

        # Remove None values from defaults to avoid overwriting existing data with None
        defaults = {k: v for k, v in defaults.items() if v is not None}

        user, created = User.objects.update_or_create(
            id=telegram_id,
            defaults=defaults
        )

        # Update last interaction
        user.last_interaction_at = timezone.now()
        user.save()

        return user
