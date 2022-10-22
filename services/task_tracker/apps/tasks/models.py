import random
import typing as ty
import uuid

from django.db import models
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from kafka_util import producer

from apps.tasks.exceptions import NoAvailablePopugs
from apps.users.models import User
from task_tracker.celery import RetryableTask

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
    title = models.CharField(max_length=100)
    jira_id = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[(x, x) for x in STATUSES], default=STATUS_IN_PROGRESS)
    executor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="tasks", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_random_user(self, choices: ty.Optional[ty.List[int]] = None):
        choices = choices or User.objects.filter(role=User.ROLE_POPUG).values_list("id", flat=True)
        if not choices:
            raise NoAvailablePopugs()
        user_id = random.choice(choices)
        self.executor_id = user_id

    def save(self, *args, **kwargs):
        if not self.executor_id:
            self.set_random_user()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.jira_id}] {self.title}"


class OutboxTable(models.Model):
    class Meta:
        db_table = "task_outbox_table"
        ordering = ["created_at"]

    topic = models.CharField(max_length=200)
    payload = models.JSONField(null=True, blank=True)
    event_name = models.CharField(max_length=200)
    version = models.SmallIntegerField()
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_init, sender=Task, dispatch_uid="task_remember_state")
def task_remember_state(instance: Task, **kwargs):
    instance._previous_executor_id = instance.executor_id
    instance._previous_status = instance.status


@receiver(post_save, sender=Task, dispatch_uid="task_create_update")
def task_create_update(instance: Task, created: bool, **kwargs):
    if created:
        OutboxTable.objects.create(
            topic="task-registered",
            payload={param: str(getattr(instance, param, "")) for param in ["public_id", "title", "jira_id", "status"]}
            | {"executor_public_id": str(instance.executor.public_id)},
            event_name="task_tracker.TaskCreated",
            version=2,
        )

    elif instance._previous_status != instance.status and instance.status == instance.STATUS_COMPLETED:
        OutboxTable.objects.create(
            topic="task-completed",
            payload={"public_id": str(instance.public_id), "executor_public_id": str(instance.executor.public_id)},
            event_name="task_tracker.TaskCompleted",
            version=1,
        )

    elif instance._previous_executor_id != instance.executor_id:
        OutboxTable.objects.create(
            topic="task-assigned",
            payload={"public_id": str(instance.public_id), "executor_public_id": str(instance.executor.public_id)},
            event_name="task_tracker.TaskAssigned",
            version=1,
        )

    else:
        OutboxTable.objects.create(
            topic="task-stream",
            payload={param: str(getattr(instance, param, "")) for param in ["public_id", "title", "jira_id", "status"]}
            | {"executor_public_id": str(instance.executor.public_id)},
            event_name="task_tracker.TaskUpdated",
            version=2,
        )
