import random
import logging
from django.utils import timezone
from apps.users.models import User
from apps.tasks.models import Task
from apps.notifications.services import send_telegram_message
from apps.notifications.models import NotificationLog
from apps.core.i18n import BackendI18n

logger = logging.getLogger(__name__)

class AntiProcrastinationService:
    @classmethod
    def trigger_reminder(cls, user):
        # Find the most overdue or oldest TODO task
        task = Task.objects.filter(assignee=user, status=Task.Status.TODO).order_by('deadline', 'created_at').first()

        if not task:
            return False

        lang = user.language
        idx = random.randint(1, 3)
        message = BackendI18n.t(lang, f"procrastination-aggressive-{idx}")

        full_message = f"⏳ <b>{message}</b>\n\nTask: {task.title}"

        success = send_telegram_message(user.id, full_message)

        NotificationLog.objects.create(
            user=user,
            type=NotificationLog.Type.ANTI_PROCRASTINATION,
            message_text=full_message,
            is_success=success
        )

        if success:
            user.last_interaction_at = timezone.now() # Update to avoid spamming too soon
            user.save()
            return True
        return False
