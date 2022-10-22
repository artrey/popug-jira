import logging

from django.db import transaction
from kafka_consumer.exceptions import ErrorMessageReceiverProcess
from kafka_util.consumer import BaseConsumer, Message

from apps.tasks.models import Task
from apps.users.models import User

logger = logging.getLogger(__name__)


class TaskConsumerV1(BaseConsumer):
    supported_version = 1
    router = {
        # TaskCreatedV1 and TaskUpdatedV1 are deprecated
        # "task_tracker.TaskCreated": "_task_created",
        # "task_tracker.TaskUpdated": "_task_updated",
        "task_tracker.TaskCompleted": "_task_completed",
        "task_tracker.TaskAssigned": "_task_assigned",
        "accounting.TaskUpdated": "_task_costs_updated",
    }

    def _update_or_create_task(self, message: Message) -> Task:
        data = message.data.get("data")
        user = User.objects.filter(public_id=data.pop("executor_public_id")).first()
        if not user:
            raise ErrorMessageReceiverProcess(f"User not found for {message=}")
        return Task.objects.update_or_create(
            public_id=data.pop("public_id"),
            defaults=data | {"executor": user},
        )

    def _task_created(self, message: Message):
        task, created = self._update_or_create_task(message)
        task.executor.account.create_transaction("outcome", task.pretty_title, credit=task.cost_assign)
        logger.info(f"Task created {task}")

    def _task_updated(self, message: Message):
        task, created = self._update_or_create_task(message)
        logger.info(f"Task updated/created {task}")

    def _task_costs_updated(self, message: Message):
        data = message.data.get("data")
        task = Task.objects.update_or_create(
            public_id=data.pop("public_id"),
            defaults=data,
        )
        logger.info(f"Task costs updated {task=}")

    def _task_completed(self, message: Message):
        data = message.data.get("data")
        task = Task.objects.filter(
            public_id=data.pop("public_id"),
            executor__public_id=data.pop("executor_public_id"),
        ).first()
        if not task:
            raise ErrorMessageReceiverProcess(f"Task with such executor not found for {message=}")

        with transaction.atomic():
            task.status = task.STATUS_COMPLETED
            task.save(update_fields=["status", "updated_at"])
            task.executor.account.create_transaction("income", task.pretty_title, debit=task.cost_complete)

        logger.info(f"Task completed {task}")

    def _task_assigned(self, message: Message):
        data = message.data.get("data")
        task = Task.objects.filter(public_id=data.pop("public_id")).first()
        if not task:
            raise ErrorMessageReceiverProcess(f"Task not found for {message=}")
        user = User.objects.filter(public_id=data.pop("executor_public_id")).first()
        if not user:
            raise ErrorMessageReceiverProcess(f"User not found for {message=}")
        if task.executor == user:
            logger.warning(f"User already executes task: {data=}")
            return

        with transaction.atomic():
            task.executor = user
            task.save(update_fields=["executor", "updated_at"])
            task.executor.account.create_transaction("outcome", task.pretty_title, credit=task.cost_assign)


class TaskConsumerV2(TaskConsumerV1):
    supported_version = 2
    router = {
        "task_tracker.TaskCreated": "_task_created",
        "task_tracker.TaskUpdated": "_task_updated",
    }
