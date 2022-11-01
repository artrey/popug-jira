from django.contrib import admin

from apps.tasks.models import OutboxTable, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["public_id", "jira_id", "title", "status", "executor"]
    list_filter = ["status", "executor"]
    list_editable = ["status"]
    search_fields = [
        "public_id",
        "jira_id",
        "title",
        "executor__username",
        "executor__first_name",
        "executor__last_name",
        "executor__public_id",
    ]
    list_select_related = ["executor"]


@admin.register(OutboxTable)
class OutboxTableAdmin(admin.ModelAdmin):
    list_display = ["id", "topic", "event_name", "version", "sent", "created_at", "updated_at"]
    list_filter = ["sent", "topic", "event_name", "version"]
    search_fields = ["topic", "event_name"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
