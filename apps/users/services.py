from datetime import timedelta
from django.utils import timezone
from django.db.models import Avg, Count
from apps.sessions.models import FocusSession
from apps.analytics.models import DailyStats
from django.db import models

class UserStyleService:
    @staticmethod
    def get_user_style(user):
        import pytz
        if user.timezone:
            timezone.activate(pytz.timezone(user.timezone))
        try:
            local_now = timezone.localtime(timezone.now())
            account_age_days = (local_now - user.created_at).days

            if account_age_days < 3:
                return {
                    "slug": "newcomer",
                    "title": "Новачок",
                    "description": "Ти тільки починаєш свій шлях до продуктивності. Ласкаво просимо!",
                    "icon": "🌱"
                }

            # Fetch some stats
            sessions = FocusSession.objects.filter(user=user, status=FocusSession.Status.COMPLETED)
            stats = sessions.aggregate(
                avg_duration=Avg('duration'),
                total_count=Count('id')
            )

            avg_duration = stats['avg_duration'] or 0
            total_count = stats['total_count'] or 0

            if total_count > 0:
                # Check for "Night Owl" (majority sessions between 21:00 and 05:00)
                night_sessions = sessions.filter(
                    models.Q(start_time__hour__gte=21) | models.Q(start_time__hour__lt=5)
                ).count()
                if night_sessions > total_count / 2:
                    return {
                        "slug": "night_owl",
                        "title": "Нічна Сова",
                        "description": "Твій мозок працює на повну, коли місто засинає.",
                        "icon": "🦉"
                    }

                # Check for "Early Bird" (majority sessions between 05:00 and 09:00)
                morning_sessions = sessions.filter(start_time__hour__gte=5, start_time__hour__lt=9).count()
                if morning_sessions > total_count / 2:
                    return {
                        "slug": "early_bird",
                        "title": "Рання Пташка",
                        "description": "Ти випереджаєш день, поки інші ще сплять.",
                        "icon": "🌅"
                    }

                # Check for "Deep Thinker"
                if avg_duration > 2700:  # > 45 min
                    return {
                        "slug": "deep_thinker",
                        "title": "Глибокий Мислитель",
                        "description": "Ти вмієш занурюватися в роботу надовго. Концентрація — твоя сила.",
                        "icon": "🧠"
                    }

            # Check for "Stable Performer" (streak >= 3)
            if user.streak >= 3:
                return {
                    "slug": "stable_performer",
                    "title": "Стабільний Виконавець",
                    "description": "Дисципліна — твоє друге ім'я. Ти тримаєш темп!",
                    "icon": "🛡️"
                }

            return {
                "slug": "explorer",
                "title": "Дослідник",
                "description": "Ти шукаєш свій ритм. Кожна сесія наближає тебе до мети.",
                "icon": "🧭"
            }
        finally:
            timezone.deactivate()
