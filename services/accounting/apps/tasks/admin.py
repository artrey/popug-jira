from django.contrib import admin

from apps.tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["public_id", "title", "cost_assign", "cost_complete", "status", "executor"]
    list_filter = ["status", "executor"]
    list_editable = ["status"]
    search_fields = [
        "public_id",
        "title",
        "executor__username",
        "executor__first_name",
        "executor__last_name",
        "executor__public_id",
    ]
    list_select_related = ["executor"]
