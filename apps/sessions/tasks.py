import logging
from django.utils import timezone
from celery import shared_task
from .models import FocusSession
from apps.notifications.services import send_telegram_message

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def notify_session_finished(self, session_id):
    try:
        session = FocusSession.objects.get(id=session_id)
        if session.status == FocusSession.Status.COMPLETED:
            return

        now = timezone.now()

        # Calculate actual focus time elapsed
        total_elapsed = (now - session.start_time).total_seconds()

        paused_duration = session.total_paused_duration
        if session.status == FocusSession.Status.PAUSED and session.last_paused_at:
            # Account for the current active pause
            current_pause = (now - session.last_paused_at).total_seconds()
            paused_duration += int(current_pause)

        actual_focus_elapsed = total_elapsed - paused_duration

        if session.status == FocusSession.Status.PAUSED:
            # If paused, we reschedule based on remaining target duration
            remaining = session.target_duration - actual_focus_elapsed
            if remaining > 0:
                self.apply_async((session_id,), countdown=remaining, task_id=f"timer_{session.id}")
            return

        # If active, check if enough focus time has passed
        if actual_focus_elapsed < session.target_duration:
            remaining = session.target_duration - actual_focus_elapsed
            self.apply_async((session_id,), countdown=remaining, task_id=f"timer_{session.id}")
            return

        # Time is up and session is active
        from apps.core.i18n import BackendI18n
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(id=session.user_id)
        lang = user.language

        title = BackendI18n.t(lang, "timer-finished")
        question = BackendI18n.t(lang, "timer-ask-completed")
        message = f"🔔 <b>{title}</b>\n{question}"

        # Build inline keyboard
        # Since we are in the backend, we manually construct the JSON structure for the keyboard
        done_text = BackendI18n.t(lang, "timer-task-done")
        continue_text = BackendI18n.t(lang, "timer-continue")
        more_text = BackendI18n.t(lang, "timer-need-more")

        task_id = str(session.task_id) if session.task_id else "None"

        reply_markup = {
            "inline_keyboard": [
                [{"text": done_text, "callback_data": f"task_done_{task_id}_{session.id}"}],
                [{"text": continue_text, "callback_data": f"timer_resume_{task_id}_{session.id}"}],
                [{"text": more_text, "callback_data": f"timer_more_{task_id}_{session.id}"}]
            ]
        }

        send_telegram_message(session.user_id, message, reply_markup=reply_markup)
    except FocusSession.DoesNotExist:
        pass
    except Exception as e:
        logger.error(f"Error notifying session finished: {e}")
