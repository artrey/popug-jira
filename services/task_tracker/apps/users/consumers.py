import logging

from kafka_util.consumer import BaseConsumer, Message

from apps.users.models import User

logger = logging.getLogger(__name__)


class UserConsumerV1(BaseConsumer):
    router = {
        "auth.UserCreated": "_user_created",
        "auth.UserUpdated": "_user_updated",
        "auth.UserDeleted": "_user_deleted",
    }

    def _should_process_message(self, message: Message):
        if not super()._should_process_message(message):
            return False
        return message.data.get("event_version") == 1

    def _user_created(self, message: Message):
        u = User.objects.create(**message.data.get("data"))
        logger.info(f"User created {u}")

    def _user_updated(self, message: Message):
        data = message.data.get("data")
        User.objects.update_or_create(public_id=data.pop("public_id"), defaults=data)
        logger.info(f"User updated/created {data=}")

    def _user_deleted(self, message: Message):
        data = message.data.get("data")
        User.objects.filter(**data).delete()
        logger.info(f"User deleted {data}")
