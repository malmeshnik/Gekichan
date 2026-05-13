from django.test import TestCase
from unittest.mock import patch
from django.utils import timezone
from datetime import datetime, timedelta
import pytz
from apps.users.models import User
from apps.tasks.models import Task
from apps.notifications.tasks import (
    hourly_notification_check,
    send_reminders,
    anti_procrastination_task
)
from apps.projects.models import Project

class NotificationTasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            id=12345678,
            first_name="Test",
            timezone="UTC"
        )
        self.project = Project.objects.create(name="Test Project", owner=self.user)
        self.task = Task.objects.create(
            title="Test Task",
            assignee=self.user,
            creator=self.user,
            project=self.project,
            status=Task.Status.TODO,
            deadline=timezone.now() + timedelta(hours=10)
        )

    @patch('apps.notifications.tasks.send_morning_message.delay')
    @patch('apps.notifications.tasks.send_daily_report.delay')
    def test_hourly_notification_check(self, mock_report, mock_morning):
        # Mock timezone to 09:00 UTC
        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = datetime(2023, 1, 1, 9, 0, 0, tzinfo=pytz.UTC)
            hourly_notification_check()
            mock_morning.assert_called_once_with(self.user.id)

        # Mock timezone to 20:00 UTC
        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = datetime(2023, 1, 1, 20, 0, 0, tzinfo=pytz.UTC)
            hourly_notification_check()
            mock_report.assert_called_once_with(self.user.id)

    @patch('apps.notifications.tasks.send_telegram_message')
    def test_send_reminders(self, mock_send):
        send_reminders()
        mock_send.assert_called()
        self.task.refresh_from_db()
        self.assertTrue(self.task.reminder_sent)

    @patch('apps.notifications.tasks.send_telegram_message')
    def test_anti_procrastination(self, mock_send):
        anti_procrastination_task()
        mock_send.assert_called_with(
            self.user.id,
            "⏳ <b>Don't wait!</b> You have tasks in TODO but haven't started any focus sessions today. Let's do at least 25 minutes?"
        )
