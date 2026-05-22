from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.core.models import BaseModel

class Task(BaseModel):
    class Status(models.TextChoices):
        TODO = "todo", "To Do"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tasks"
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    deadline = models.DateTimeField(null=True, blank=True)
    reminder_24h_sent = models.BooleanField(default=False)
    reminder_1h_sent = models.BooleanField(default=False)
    overdue_reminder_sent = models.BooleanField(default=False)

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["project", "status"]),
            models.Index(fields=["assignee", "status"]),
            models.Index(fields=["creator", "status"]),
        ]

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):

        if (
            self.status == self.Status.IN_PROGRESS
            and not self.started_at
        ):
            self.started_at = timezone.now()

        if self.status == self.Status.DONE:

            if not self.completed_at:
                self.completed_at = timezone.now()

        else:
            self.completed_at = None

        super().save(*args, **kwargs)

class TaskAttachment(BaseModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="attachments"
    )
    file = models.FileField(upload_to="task_attachments/", null=True, blank=True)
    telegram_file_id = models.CharField(max_length=255, null=True, blank=True)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    mime_type = models.CharField(max_length=100, null=True, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_attachments"
    )

    def __str__(self):
        return self.file_name or self.telegram_file_id
