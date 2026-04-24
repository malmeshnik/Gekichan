from django.utils import timezone
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from .models import FocusSession
from apps.tasks.models import Task
from apps.projects.models import ProjectMember

def start_focus_session(user, task_id=None, context=None):
    # Check if user already has an active session
    if FocusSession.objects.filter(user=user, end_time__isnull=True).exists():
        raise ValidationError("You already have an active session.")

    task = None
    if task_id:
        try:
            task = Task.objects.get(id=task_id)
        except (Task.DoesNotExist, ValueError):
            raise ValidationError("Task does not exist.")

        # Check access: assignee or project member
        is_assignee = task.assignee == user
        is_member = ProjectMember.objects.filter(project=task.project, user=user).exists()

        if not (is_assignee or is_member):
            raise PermissionDenied("You do not have access to this task.")

    session = FocusSession.objects.create(
        user=user,
        task=task,
        start_time=timezone.now(),
        context=context or FocusSession.Context.WORK,
        interruptions_count=0
    )
    return session

def stop_focus_session(user, session_id):
    try:
        session = FocusSession.objects.get(id=session_id, user=user)
    except (FocusSession.DoesNotExist, ValueError):
        raise ValidationError("Session not found.")

    if session.end_time is not None:
        raise ValidationError("Session is not active.")

    session.end_time = timezone.now()
    duration_delta = session.end_time - session.start_time
    session.duration = int(duration_delta.total_seconds())
    session.save()
    return session

def pause_focus_session(user, session_id):
    try:
        session = FocusSession.objects.get(id=session_id, user=user)
    except (FocusSession.DoesNotExist, ValueError):
        raise ValidationError("Session not found.")

    if session.end_time is not None:
        raise ValidationError("Session is not active.")

    session.interruptions_count += 1
    session.save()
    return session
