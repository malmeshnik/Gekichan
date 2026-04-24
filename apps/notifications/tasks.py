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

logger = logging.getLogger(__name__)

@shared_task
def hourly_notification_check():
    """
    Runs every hour to check which users should receive morning or daily reports
    based on their timezone.
    """
    now_utc = timezone.now()
    users = User.objects.filter(is_active=True, deleted_at__isnull=True)

    for user in users:
        try:
            user_tz = pytz.timezone(user.timezone)
            user_now = now_utc.astimezone(user_tz)

            # Check for Morning Message (09:00)
            if user_now.hour == 9:
                send_morning_message.delay(user.id)

            # Check for Daily Report (20:00)
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

        # 1. Get Today's Stats
        stats_today = DailyStats.objects.filter(user=user, date=today).first()
        if not stats_today:
            # Fallback calculation
            sessions = FocusSession.objects.filter(
                user=user,
                start_time__date=today,
                end_time__isnull=False
            )
            total_focus_time = sessions.aggregate(Sum('duration'))['duration__sum'] or 0
            interruptions = sessions.aggregate(Sum('interruptions_count'))['interruptions_count__sum'] or 0
            tasks_done = Task.objects.filter(assignee=user, status=Task.Status.DONE, updated_at__date=today).count()
        else:
            total_focus_time = stats_today.total_focus_time
            interruptions = stats_today.interruptions_count
            tasks_done = stats_today.completed_tasks_count

        # 2. Get Yesterday's Stats for comparison
        stats_yesterday = DailyStats.objects.filter(user=user, date=yesterday).first()

        focus_h = total_focus_time / 3600

        message = (
            f"📊 <b>Your day:</b>\n"
            f"- focus time: {focus_h:.1f}h\n"
            f"- tasks done: {tasks_done}\n"
            f"- interruptions: {interruptions}\n"
        )

        if stats_yesterday and stats_yesterday.total_focus_time > 0:
            change = ((total_focus_time - stats_yesterday.total_focus_time) / stats_yesterday.total_focus_time) * 100
            symbol = "+" if change >= 0 else ""
            message += f"- % change: {symbol}{change:.1f}% vs yesterday"

        send_telegram_message(user.id, message)

    except Exception as e:
        logger.error(f"Error in send_daily_report for user {user_id}: {e}")

@shared_task
def send_morning_message(user_id):
    try:
        user = User.objects.get(id=user_id)
        user_tz = pytz.timezone(user.timezone)
        yesterday = (timezone.now().astimezone(user_tz) - timedelta(days=1)).date()

        stats_yesterday = DailyStats.objects.filter(user=user, date=yesterday).first()

        if stats_yesterday:
            yesterday_h = stats_yesterday.total_focus_time / 3600
            goal_h = yesterday_h * 1.1

            message = (
                f"🌅 <b>Good morning!</b>\n"
                f"- yesterday: {yesterday_h:.1f}h\n"
                f"- today goal: {goal_h:.1f}h (+10%)"
            )
        else:
            message = "🌅 <b>Good morning!</b>\nReady for a productive day? Set your first goal!"

        send_telegram_message(user.id, message)

    except Exception as e:
        logger.error(f"Error in send_morning_message for user {user_id}: {e}")

@shared_task
def send_reminders():
    now = timezone.now()
    upcoming_limit = now + timedelta(hours=24)

    # Upcoming tasks (next 24h)
    upcoming_tasks = Task.objects.filter(
        status__in=[Task.Status.TODO, Task.Status.IN_PROGRESS],
        deadline__gt=now,
        deadline__lte=upcoming_limit,
        reminder_sent=False
    )

    for task in upcoming_tasks:
        if task.assignee:
            message = f"⏰ <b>Reminder:</b> Task \"{task.title}\" is due within 24 hours!"
            if send_telegram_message(task.assignee.id, message):
                task.reminder_sent = True
                task.save()

    # Overdue tasks
    overdue_tasks = Task.objects.filter(
        status__in=[Task.Status.TODO, Task.Status.IN_PROGRESS],
        deadline__lt=now,
        reminder_sent=False
    )

    for task in overdue_tasks:
        if task.assignee:
            message = f"🚨 <b>Overdue:</b> Task \"{task.title}\" is past its deadline!"
            if send_telegram_message(task.assignee.id, message):
                task.reminder_sent = True
                task.save()

@shared_task
def anti_procrastination_task():
    users = User.objects.filter(is_active=True, deleted_at__isnull=True)
    now = timezone.now()

    for user in users:
        user_tz = pytz.timezone(user.timezone)
        today = now.astimezone(user_tz).date()

        # Check if any session started today
        has_sessions_today = FocusSession.objects.filter(user=user, start_time__date=today).exists()

        # Check if has pending tasks
        has_pending_tasks = Task.objects.filter(assignee=user, status=Task.Status.TODO).exists()

        if not has_sessions_today and has_pending_tasks:
            message = "⏳ <b>Don't wait!</b> You have tasks in TODO but haven't started any focus sessions today. Let's do at least 25 minutes?"
            send_telegram_message(user.id, message)
