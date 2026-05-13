from django.contrib import admin
from .models import Project, ProjectMember

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at", "deleted_at")
    search_fields = ("name", "owner__username", "owner__first_name")
    list_filter = ("created_at", "deleted_at")

@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ("project", "user", "role", "created_at")
    list_filter = ("role", "created_at")
    search_fields = ("project__name", "user__username", "user__first_name")
