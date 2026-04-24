from django.db import models
from django.conf import settings
from apps.core.models import BaseModel

class Task(BaseModel):
    class Status(models.TextChoices):
        TODO = "todo", "To Do"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="tasks"
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
    deadline = models.DateTimeField(null=True, blank=True)
    reminder_sent = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["project", "status"]),
            models.Index(fields=["assignee", "status"]),
        ]

    def __str__(self):
        return self.title
