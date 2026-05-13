import logging
from datetime import datetime, timedelta
import pytz
from django.utils import timezone
from django.db.models import Sum, Count
from celery import shared_task
from apps.users.models import User
from apps.analytics.models import DailyStats
from apps.sessions.models import FocusSession
from apps.tasks.models import Task
from .services import send_telegram_message
from .anti_procrastination import AntiProcrastinationService
from apps.core.i18n import BackendI18n

logger = logging.getLogger(__name__)

@shared_task
def hourly_notification_check():
    now_utc = timezone.now()
    # Only active users who haven't been deleted
    users = User.objects.filter(is_active=True, deleted_at__isnull=True)

    for user in users:
        try:
            user_tz = pytz.timezone(user.timezone)
            user_now = now_utc.astimezone(user_tz)

            if user_now.hour == 9:
                send_morning_message.delay(user.id)

            if user_now.hour == 20:
                send_daily_report.delay(user.id)
        except Exception as e:
            logger.error(f"Error checking notifications for user {user.id}: {e}")

@shared_task
def send_daily_report(user_id):
    try:
        user = User.objects.get(id=user_id)
        user_tz = pytz.timezone(user.timezone)
        today = timezone.now().astimezone(user_tz).date()
        yesterday = today - timedelta(days=1)

        stats_today = DailyStats.objects.filter(user=user, date=today).first()
        if not stats_today:
            sessions = FocusSession.objects.filter(user=user, start_time__date=today, status=FocusSession.Status.COMPLETED)
            total_focus_time = sessions.aggregate(Sum('duration'))['duration__sum'] or 0
            interruptions = sessions.aggregate(Sum('interruptions_count'))['interruptions_count__sum'] or 0
            tasks_done = Task.objects.filter(assignee=user, status=Task.Status.DONE, updated_at__date=today).count()
        else:
            total_focus_time = stats_today.total_focus_time
            interruptions = stats_today.interruptions_count
            tasks_done = stats_today.completed_tasks_count

        focus_h = total_focus_time / 3600
        lang = user.language

        title = BackendI18n.t(lang, "stats-daily-title")
        focus_label = BackendI18n.t(lang, "stats-focus-label")
        tasks_label = BackendI18n.t(lang, "stats-tasks-label")
        interr_label = BackendI18n.t(lang, "stats-interruptions-label")

        message = (
            f"📊 <b>{title}:</b>\n"
            f"- {focus_label}: {focus_h:.1f}h\n"
            f"- {tasks_label}: {tasks_done}\n"
            f"- {interr_label}: {interruptions}\n"
        )

        send_telegram_message(user.id, message)
    except Exception as e:
        logger.error(f"Error in send_daily_report for user {user_id}: {e}")

@shared_task
def send_morning_message(user_id):
    try:
        user = User.objects.get(id=user_id)
        lang = user.language

        welcome = BackendI18n.t(lang, "start-welcome", name=user.first_name)
        help_text = BackendI18n.t(lang, "start-help")

        message = f"🌅 <b>{welcome}</b>\n{help_text}"
        send_telegram_message(user.id, message)
    except Exception as e:
        logger.error(f"Error in send_morning_message for user {user_id}: {e}")

@shared_task
def send_reminders():
    now = timezone.now()

    # 24h reminders
    limit_24h = now + timedelta(hours=24)
    tasks_24h = Task.objects.filter(
        status__in=[Task.Status.TODO, Task.Status.IN_PROGRESS],
        deadline__gt=now,
        deadline__lte=limit_24h,
        reminder_24h_sent=False
    ).select_related('assignee')
    for task in tasks_24h:
        if task.assignee:
            lang = task.assignee.language
            text = BackendI18n.t(lang, "reminder-deadline-24h", title=task.title)
            if send_telegram_message(task.assignee.id, f"⏰ <b>{text}</b>"):
                task.reminder_24h_sent = True
                task.save()

    # 1h reminders
    limit_1h = now + timedelta(hours=1)
    tasks_1h = Task.objects.filter(
        status__in=[Task.Status.TODO, Task.Status.IN_PROGRESS],
        deadline__gt=now,
        deadline__lte=limit_1h,
        reminder_1h_sent=False
    ).select_related('assignee')
    for task in tasks_1h:
        if task.assignee:
            lang = task.assignee.language
            text = BackendI18n.t(lang, "reminder-deadline-1h", title=task.title)
            if send_telegram_message(task.assignee.id, f"🚨 <b>{text}</b>"):
                task.reminder_1h_sent = True
                task.save()

    # Overdue reminders
    overdue_tasks = Task.objects.filter(
        status__in=[Task.Status.TODO, Task.Status.IN_PROGRESS],
        deadline__lt=now,
        overdue_reminder_sent=False
    ).select_related('assignee')
    for task in overdue_tasks:
        if task.assignee:
            lang = task.assignee.language
            text = BackendI18n.t(lang, "reminder-overdue", title=task.title)
            if send_telegram_message(task.assignee.id, f"🔥 <b>{text}</b>"):
                task.overdue_reminder_sent = True
                task.save()

@shared_task
def anti_procrastination_task():
    # Only check users who have been inactive for at least 4 hours
    threshold = timezone.now() - timedelta(hours=4)
    users = User.objects.filter(
        is_active=True,
        deleted_at__isnull=True,
        last_interaction_at__lte=threshold
    )

    for user in users:
        AntiProcrastinationService.trigger_reminder(user)
