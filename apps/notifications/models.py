from django.db import models
from django.conf import settings
from apps.core.models import BaseModel

class NotificationLog(BaseModel):
    class Type(models.TextChoices):
        REMINDER = "reminder", "Reminder"
        ANTI_PROCRASTINATION = "anti_procrastination", "Anti-Procrastination"
        BROADCAST = "broadcast", "Broadcast"
        SYSTEM = "system", "System"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_logs"
    )
    type = models.CharField(max_length=50, choices=Type.choices)
    message_text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Notification Log"
        verbose_name_plural = "Notification Logs"

class Mailing(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENDING = "sending", "Sending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    subject = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    inactive_days_filter = models.IntegerField(null=True, blank=True, help_text="Send only to users inactive for more than X days")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total_recipients = models.IntegerField(default=0)
    sent_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Mailing {self.id} - {self.status}"
