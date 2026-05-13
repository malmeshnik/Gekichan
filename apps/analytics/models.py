from django.db import models
from django.conf import settings
from apps.core.models import BaseModel

class DailyStats(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="daily_stats"
    )
    date = models.DateField()
    total_focus_time = models.IntegerField(default=0, help_text="Total focus time in seconds")
    completed_tasks_count = models.IntegerField(default=0)
    interruptions_count = models.IntegerField(default=0)
    productivity_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ("user", "date")
        verbose_name_plural = "Daily stats"

    def __str__(self):
        return f"{self.user} - {self.date}"
