from django.contrib import admin
from .models import NotificationLog, Mailing
from .tasks import send_mass_mailing

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "sent_at", "is_success")
    list_filter = ("type", "is_success", "sent_at")
    search_fields = ("user__username", "user__first_name", "message_text")
    readonly_fields = ("sent_at",)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "sent_count", "total_recipients", "started_at")
    list_filter = ("status", "started_at")
    readonly_fields = ("total_recipients", "sent_count", "error_count", "started_at", "completed_at")
    actions = ["trigger_mailing"]

    def trigger_mailing(self, request, queryset):
        for mailing in queryset:
            if mailing.status == Mailing.Status.PENDING:
                send_mass_mailing.delay(mailing.id)
                self.message_user(request, f"Mailing {mailing.id} has been queued.")
            else:
                self.message_user(request, f"Mailing {mailing.id} is already in progress or completed.", level="warning")

    trigger_mailing.short_description = "Start mass mailing"
