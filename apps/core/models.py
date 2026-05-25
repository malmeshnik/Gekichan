import uuid
from django.db import models
from django.utils import timezone
from solo.models import SingletonModel

class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.exclude(deleted_at__isnull=True)

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()

    def all_with_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db)

    def deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db).dead()

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()

class BotSettings(SingletonModel):
    xp_per_task = models.IntegerField(default=10, help_text="XP awarded for completing a task")
    free_projects_limit = models.IntegerField(default=3, help_text="Maximum number of free projects per user")
    anti_procrastination_threshold = models.IntegerField(default=3, help_text="Hours of inactivity before anti-procrastination trigger")
    maintenance_mode = models.BooleanField(default=False)
    broadcast_enabled = models.BooleanField(default=True)

    def __str__(self):
        return "Global Bot Settings"

    class Meta:
        verbose_name = "Bot Settings"
