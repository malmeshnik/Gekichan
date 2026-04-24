from django.db import models
from django.conf import settings
from apps.core.models import BaseModel

class FocusSession(BaseModel):
    class Context(models.TextChoices):
        WORK = "work", "Work"
        STUDY = "study", "Study"
        CUSTOM = "custom", "Custom"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="focus_sessions"
    )
    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="focus_sessions"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=0, help_text="Duration in seconds")
    interruptions_count = models.IntegerField(default=0)
    context = models.CharField(
        max_length=50,
        choices=Context.choices,
        default=Context.WORK
    )

    class Meta:
        indexes = [
            models.Index(fields=["user", "start_time"]),
        ]

    def __str__(self):
        return f"Session {self.id} - {self.user}"
