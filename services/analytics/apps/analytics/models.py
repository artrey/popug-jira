import uuid

from django.db import models

from apps.tasks.models import Task


class TaskEvent(models.Model):
    EVENT_TYPE_ASSIGN = "assign"
    EVENT_TYPE_COMPLETE = "complete"
    EVENT_TYPES = (
        EVENT_TYPE_ASSIGN,
        EVENT_TYPE_COMPLETE,
    )

    public_id = models.UUIDField(default=uuid.uuid4, unique=True)
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING, related_name="events")
    type = models.CharField(max_length=20, choices=[(x, x) for x in EVENT_TYPES])
    created_at = models.DateTimeField(auto_now_add=True)
