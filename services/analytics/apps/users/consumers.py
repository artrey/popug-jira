import logging

from kafka_util.consumer import BaseConsumer, Message

from apps.users.models import User

logger = logging.getLogger(__name__)


class UserConsumerV1(BaseConsumer):
    supported_version = 1
    router = {
        "auth.UserCreated": "_user_created_or_updated",
        "auth.UserUpdated": "_user_created_or_updated",
        "auth.UserDeleted": "_user_deleted",
    }

    def _user_created_or_updated(self, message: Message):
        data = message.data.get("data")
        User.objects.update_or_create(public_id=data.pop("public_id"), defaults=data)
        logger.info(f"User updated/created {data=}")

    def _user_deleted(self, message: Message):
        data = message.data.get("data")
        User.objects.filter(**data).delete()
        logger.info(f"User deleted {data}")
