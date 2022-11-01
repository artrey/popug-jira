import typing as ty

from django.contrib import admin

from apps.analytics.models import TaskEvent


@admin.register(TaskEvent)
class TaskEventAdmin(admin.ModelAdmin):
    list_display = ["public_id", "task", "task_cost_assign", "task_cost_complete", "type", "created_at"]
    list_filter = ["type", "created_at"]
    list_select_related = ["task"]
    readonly_fields = ["task", "task_cost_assign", "task_cost_complete"]

    @admin.display
    def task_cost_assign(self, task_event: TaskEvent) -> ty.Optional[int]:
        return task_event.task.cost_assign

    @admin.display
    def task_cost_complete(self, task_event: TaskEvent) -> ty.Optional[int]:
        return task_event.task.cost_complete
