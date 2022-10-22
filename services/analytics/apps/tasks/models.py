import uuid

from django.db import models
from kafka_util import producer

from analytics.celery import RetryableTask
from apps.users.models import User

send_event = RetryableTask(producer.send_event)


class Task(models.Model):
    class Meta:
        db_table = "tasks"

    STATUS_IN_PROGRESS = "В работе"
    STATUS_COMPLETED = "Завершена"
    STATUSES = (
        STATUS_IN_PROGRESS,
        STATUS_COMPLETED,
    )

    public_id = models.UUIDField(default=uuid.uuid4, unique=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    jira_id = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[(x, x) for x in STATUSES], null=True, blank=True)
    executor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="tasks", null=True, blank=True)
    cost_assign = models.PositiveIntegerField(null=True, blank=True)
    cost_complete = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def pretty_title(self) -> str:
        return f"[{self.jira_id}] {self.title}"

    def __str__(self):
        return self.pretty_title
