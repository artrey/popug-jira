import random
import uuid

from django.db import models

from apps.users.models import User


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
    title = models.CharField(max_length=100)
    jira_id = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=[(x, x) for x in STATUSES], default=STATUS_IN_PROGRESS)
    executor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="tasks")
    cost_assign = models.PositiveIntegerField()
    cost_complete = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.cost_assign:
            self.cost_assign = random.randint(10, 20)
        if not self.cost_complete:
            self.cost_assign = random.randint(20, 40)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title