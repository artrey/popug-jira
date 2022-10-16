import random
import typing as ty
import uuid

from django.db import models
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from kafka_util import producer

from apps.tasks.exceptions import NoAvailablePopugs
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


@receiver(post_init, sender=Task, dispatch_uid="task_remember_state")
def task_remember_state(instance: Task, **kwargs):
    instance._previous_executor_id = instance.executor_id
    instance._previous_status = instance.status


@receiver(post_save, sender=Task, dispatch_uid="task_create_update")
def task_create_update(instance: Task, created: bool, **kwargs):
    # TODO: think about batch sending

    if created:
        producer.send_event(
            "task-registered",
            {param: str(getattr(instance, param, "")) for param in ["public_id", "title", "jira_id", "status"]}
            | {"executor_public_id": str(instance.executor.public_id)},
            "task_tracker.TaskCreated",
            2,
        )

    elif instance._previous_status != instance.status and instance.status == instance.STATUS_COMPLETED:
        producer.send_event(
            "task-completed",
            {"public_id": str(instance.public_id), "executor_public_id": str(instance.executor.public_id)},
            "task_tracker.TaskCompleted",
            1,
        )

    elif instance._previous_executor_id != instance.executor_id:
        producer.send_event(
            "task-assigned",
            {"public_id": str(instance.public_id), "executor_public_id": str(instance.executor.public_id)},
            "task_tracker.TaskAssigned",
            1,
        )

    else:
        producer.send_event(
            "task-stream",
            {param: str(getattr(instance, param, "")) for param in ["public_id", "title", "jira_id", "status"]}
            | {"executor_public_id": str(instance.executor.public_id)},
            "task_tracker.TaskUpdated",
            2,
        )
