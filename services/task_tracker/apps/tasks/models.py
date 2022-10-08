import random
import typing as ty
import uuid

from django.db import models
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver

import apps.kafka_util.proto as kafka_proto
from apps import kafka_util
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
        return self.title


@receiver(post_init, sender=Task, dispatch_uid="task_remember_executor")
def task_remember_executor(instance: Task, **kwargs):
    instance._previous_executor = instance.executor


@receiver(post_save, sender=Task, dispatch_uid="task_create_update")
def task_create_update(instance: Task, created: bool, **kwargs):
    def build_message(event_type: kafka_proto.EventType) -> kafka_proto.Message:
        return kafka_proto.Message(
            entity="task",
            event=event_type,
            public_id=str(instance.public_id),
            data=kafka_proto.Task(
                **{
                    param: getattr(instance, param)
                    for param in [
                        "title",
                        "status",
                        "created_at",
                        "updated_at",
                    ]
                },
                executor_public_id=str(instance.executor.public_id),
            ),
        )

    if created:
        kafka_util.send_message("task-registered", build_message(kafka_proto.EventType.BUSINESS))
    elif instance.status == Task.STATUS_COMPLETED:
        kafka_util.send_message("task-completed", build_message(kafka_proto.EventType.BUSINESS))
    elif instance._previous_executor != instance.executor:
        kafka_util.send_message("task-assigned", build_message(kafka_proto.EventType.BUSINESS))
    else:
        kafka_util.send_message("task-streaming", build_message(kafka_proto.EventType.UPDATE))
