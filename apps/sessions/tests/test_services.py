from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from apps.sessions.models import FocusSession
from apps.sessions.services import start_focus_session, stop_focus_session, pause_focus_session
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
        session = start_focus_session(user=self.user, task_id=self.task.id)
        self.assertEqual(session.user, self.user)
        self.assertEqual(session.task, self.task)
        self.assertIsNone(session.end_time)
        self.assertEqual(session.interruptions_count, 0)

    def test_start_session_already_active_fails(self):
        start_focus_session(user=self.user)
        with self.assertRaises(ValidationError) as cm:
            start_focus_session(user=self.user)
        self.assertEqual(str(cm.exception.detail[0]), "You already have an active session.")

    def test_start_session_unauthorized_task_fails(self):
        # other_user is NOT assignee and NOT project member
        with self.assertRaises(PermissionDenied):
            start_focus_session(user=self.other_user, task_id=self.task.id)

    def test_start_session_project_member_success(self):
        ProjectMember.objects.create(project=self.project, user=self.other_user, role=ProjectMember.Role.MEMBER)
        # Now other_user is a project member, should be able to start session on task
        session = start_focus_session(user=self.other_user, task_id=self.task.id)
        self.assertEqual(session.user, self.other_user)

    def test_stop_session_success(self):
        session = start_focus_session(user=self.user)
        stopped_session = stop_focus_session(user=self.user, session_id=session.id)
        self.assertIsNotNone(stopped_session.end_time)
        self.assertGreaterEqual(stopped_session.duration, 0)

    def test_stop_inactive_session_fails(self):
        session = start_focus_session(user=self.user)
        stop_focus_session(user=self.user, session_id=session.id)
        with self.assertRaises(ValidationError) as cm:
            stop_focus_session(user=self.user, session_id=session.id)
        self.assertEqual(str(cm.exception.detail[0]), "Session is not active.")

    def test_pause_session_success(self):
        session = start_focus_session(user=self.user)
        paused_session = pause_focus_session(user=self.user, session_id=session.id)
        self.assertEqual(paused_session.interruptions_count, 1)

        pause_focus_session(user=self.user, session_id=session.id)
        paused_session.refresh_from_db()
        self.assertEqual(paused_session.interruptions_count, 2)
        self.assertIsNone(paused_session.end_time)

    def test_pause_inactive_session_fails(self):
        session = start_focus_session(user=self.user)
        stop_focus_session(user=self.user, session_id=session.id)
        with self.assertRaises(ValidationError) as cm:
            pause_focus_session(user=self.user, session_id=session.id)
        self.assertEqual(str(cm.exception.detail[0]), "Session is not active.")

    def test_session_ownership(self):
        session = start_focus_session(user=self.user)
        with self.assertRaises(ValidationError) as cm:
            stop_focus_session(user=self.other_user, session_id=session.id)
        self.assertEqual(str(cm.exception.detail[0]), "Session not found.")
