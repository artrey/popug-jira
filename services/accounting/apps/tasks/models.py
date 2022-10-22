import random
import uuid

from django.db import models
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver

from apps.users.models import User
from apps.util import send_event


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
            self.cost_complete = random.randint(20, 40)
        return super().save(*args, **kwargs)

    @property
    def pretty_title(self) -> str:
        return f"[{self.jira_id}] {self.title}"

    def __str__(self):
        return self.pretty_title


@receiver(post_init, sender=Task, dispatch_uid="task_remember_state")
def task_remember_state(instance: Task, **kwargs):
    instance._previous_cost_assign = instance.cost_assign
    instance._previous_cost_complete = instance.cost_complete


@receiver(post_save, sender=Task, dispatch_uid="task_create_update")
def task_create_update(instance: Task, **kwargs):
    if (
        instance._previous_cost_assign != instance.cost_assign
        or instance._previous_cost_complete != instance.cost_complete
    ):
        send_event(
            "task-stream",
            {param: str(getattr(instance, param, "")) for param in ["public_id", "cost_assign", "cost_complete"]},
            "accounting.TaskUpdated",
            1,
            raise_error=True,
        )
