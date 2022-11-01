import logging

from kafka_consumer.exceptions import ErrorMessageReceiverProcess
from kafka_util.consumer import BaseConsumer, Message

from apps.accounts.models import Account
from apps.users.models import User

logger = logging.getLogger(__name__)


class AccountConsumerV1(BaseConsumer):
    supported_version = 1
    router = {
        "accounting.AccountCreated": "_account_created_or_updated",
        "accounting.AccountUpdated": "_account_created_or_updated",
    }

    def _account_created_or_updated(self, message: Message):
        data = message.data.get("data")
        user = User.objects.filter(public_id=data.pop("owner_public_id")).first()
        if not user:
            raise ErrorMessageReceiverProcess(f"User not found for {message=}")
        Account.objects.update_or_create(public_id=data.pop("public_id"), defaults=data | {"user": user})
        logger.info(f"Account updated/created {data=}")
