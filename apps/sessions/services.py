from typing import Optional, Union
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django.db import transaction
from apps.users.models import User
from .models import FocusSession
from apps.tasks.models import Task
from apps.projects.models import ProjectMember

class FocusSessionService:
    @staticmethod
    def start_session(
        user: User,
        task_id: Optional[Union[str, int]] = None,
        target_duration: Optional[int] = None,
        context: Optional[str] = None
    ) -> FocusSession:
        # Check for active session
        if FocusSession.objects.filter(user=user, status__in=[FocusSession.Status.ACTIVE, FocusSession.Status.PAUSED]).exists():
            raise ValidationError("You already have an active session.")

        task = None
        if task_id:
            task = Task.objects.get(id=task_id)
            # Permission check already handled in view or can be added here

        session = FocusSession.objects.create(
            user=user,
            task=task,
            start_time=timezone.now(),
            target_duration=target_duration,
            context=context or FocusSession.Context.WORK,
            status=FocusSession.Status.ACTIVE
        )

        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Focus session started: {session.id} for user {user.id}")

        if target_duration:
            from .tasks import notify_session_finished
            # Use a task ID linked to session to allow revoking if needed
            notify_session_finished.apply_async(
                (str(session.id),),
                countdown=target_duration,
                task_id=f"timer_{session.id}"
            )

        return session

    @staticmethod
    def pause_session(user: User, session_id: Union[str, int]) -> FocusSession:
        session = FocusSession.objects.get(id=session_id, user=user)
        if session.status != FocusSession.Status.ACTIVE:
            raise ValidationError("Session is not active.")

        session.status = FocusSession.Status.PAUSED
        session.last_paused_at = timezone.now()
        session.interruptions_count += 1
        session.save()

        # If it was a countdown, we should ideally adjust the notification.
        # For MVP, we'll just let it trigger and the task will check if it's still active.
        return session

    @staticmethod
    def resume_session(user: User, session_id: Union[str, int]) -> FocusSession:
        session = FocusSession.objects.get(id=session_id, user=user)
        if session.status != FocusSession.Status.PAUSED:
            raise ValidationError("Session is not paused.")

        paused_delta = timezone.now() - session.last_paused_at
        session.total_paused_duration += int(paused_delta.total_seconds())
        session.status = FocusSession.Status.ACTIVE
        session.last_paused_at = None
        session.save()
        return session

    @staticmethod
    def stop_session(user: User, session_id: Union[str, int]) -> FocusSession:
        session = FocusSession.objects.get(id=session_id, user=user)
        if session.status == FocusSession.Status.COMPLETED:
            raise ValidationError("Session already completed.")

        now = timezone.now()
        if session.status == FocusSession.Status.PAUSED:
            # Add final pause time
            paused_delta = now - session.last_paused_at
            session.total_paused_duration += int(paused_delta.total_seconds())

        session.end_time = now
        total_delta = session.end_time - session.start_time
        session.duration = int(total_delta.total_seconds()) - session.total_paused_duration
        session.status = FocusSession.Status.COMPLETED
        session.save()

        # Update daily stats
        from apps.analytics.services import update_daily_stats
        stats = update_daily_stats(user, session.duration, session.interruptions_count)

        # Attach productivity score to session object for easy access in view
        session.productivity_score = stats.productivity_score

        return session
