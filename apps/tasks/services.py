from typing import Optional, Union
from django.utils import timezone
from django.db import models
from apps.users.models import User
from .models import Task
from apps.analytics.services import update_daily_stats

class TaskService:
    @staticmethod
    def create_task(
        user: User,
        project_id: Union[str, int],
        title: str,
        description: Optional[str] = None,
        deadline: Optional[timezone.datetime] = None,
        assignee_id: Optional[int] = None
    ) -> Task:
        # Soft delete check is automatic via SoftDeleteManager
        task = Task.objects.create(
            project_id=project_id,
            creator=user,
            title=title,
            description=description,
            deadline=deadline,
            assignee_id=assignee_id or user.id
        )
        return task

    @staticmethod
    def update_status(user: User, task_id: Union[str, int], status: str) -> Task:
        # Access check: assignee or project owner/member
        task = Task.objects.get(
            models.Q(id=task_id) & (
                models.Q(assignee=user) |
                models.Q(project__owner=user) |
                models.Q(project__members__user=user)
            )
        )

        old_status = task.status
        task.status = status
        task.save()

        if status == Task.Status.DONE and old_status != Task.Status.DONE:
            update_daily_stats(task.assignee or user, 0, 0, tasks_completed=1)

        return task

    @staticmethod
    def delete_task(user: User, task_id: Union[str, int]) -> bool:
        # Only creator or project owner can delete
        task = Task.objects.get(
            models.Q(id=task_id) & (
                models.Q(creator=user) |
                models.Q(project__owner=user)
            )
        )
        task.delete()
        return True
