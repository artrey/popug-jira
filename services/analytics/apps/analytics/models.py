import uuid

from django.db import models

from apps.tasks.models import Task


class TaskEvent(models.Model):
    EVENT_TYPE_DEBIT = "debit"
    EVENT_TYPE_CREDIT = "credit"
    EVENT_TYPES = (
        EVENT_TYPE_DEBIT,
        EVENT_TYPE_CREDIT,
    )

    public_id = models.UUIDField(default=uuid.uuid4, unique=True)
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING, related_name="events")
    type = models.CharField(max_length=20, choices=[(x, x) for x in EVENT_TYPES])
    created_at = models.DateTimeField(auto_now_add=True)
