from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from apps.sessions.models import FocusSession
from apps.sessions.services import FocusSessionService
from apps.tasks.models import Task
from apps.projects.models import Project, ProjectMember

User = get_user_model()

class FocusSessionServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(id=12345, first_name="Test", username="testuser")
        self.other_user = User.objects.create_user(id=67890, first_name="Other", username="otheruser")
        self.project = Project.objects.create(name="Test Project", owner=self.user)
        self.task = Task.objects.create(
            title="Test Task",
            project=self.project,
            creator=self.user,
            assignee=self.user
        )

    def test_start_session_success(self):
        session = FocusSessionService.start_session(user=self.user, task_id=self.task.id)
        self.assertEqual(session.user, self.user)
        self.assertEqual(session.task, self.task)
        self.assertIsNone(session.end_time)
        self.assertEqual(session.interruptions_count, 0)

    def test_start_session_already_active_fails(self):
        FocusSessionService.start_session(user=self.user)
        with self.assertRaises(ValidationError) as cm:
            FocusSessionService.start_session(user=self.user)
        self.assertEqual(str(cm.exception.detail[0]), "You already have an active session.")

    def test_stop_session_success(self):
        session = FocusSessionService.start_session(user=self.user)
        stopped_session = FocusSessionService.stop_session(user=self.user, session_id=session.id)
        self.assertIsNotNone(stopped_session.end_time)
        self.assertGreaterEqual(stopped_session.duration, 0)

    def test_pause_session_success(self):
        session = FocusSessionService.start_session(user=self.user)
        paused_session = FocusSessionService.pause_session(user=self.user, session_id=session.id)
        self.assertEqual(paused_session.interruptions_count, 1)

    def test_session_ownership(self):
        session = FocusSessionService.start_session(user=self.user)
        with self.assertRaises(FocusSession.DoesNotExist):
            FocusSessionService.stop_session(user=self.other_user, session_id=session.id)
