import abc
import datetime as dt
import logging
import typing as ty
from functools import cached_property

from django.conf import settings
from kafka_consumer.messages import BaseMessageProcessor
from kafka_consumer.messages import Message as BaseMessage
from kafka_consumer.subscribers.base import BaseSubscriber

from kafka_util.serializers import json_deserialize

logger = logging.getLogger(__name__)


class Message(BaseMessage):
    def __init__(self, message_processor: "MessageProcessor", offset: int = 0):
        self.message_processor = message_processor
        self.offset = offset

    @cached_property
    def valid(self) -> bool:
        return self.message_processor.get_valid()

    @cached_property
    def type(self) -> ty.Union[str, int]:
        return self.message_processor.get_type()

    @cached_property
    def time(self) -> dt.datetime:
        return self.message_processor.get_time()

    @cached_property
    def data(self) -> dict:
        return self.message_processor.get_data()

    def __str__(self) -> str:
        return f"Message(time={self.time}, type={self.type}, data={self.data})"


class MessageProcessor(BaseMessageProcessor):
    MESSAGE_CLASS = Message

    @cached_property
    def decoded_data(self) -> dict:
        return json_deserialize(self._kafka_message)

    def get_valid(self) -> bool:
        event_name = self.decoded_data.get("event_name")
        version = self.decoded_data.get("event_version")
        return settings.SCHEME_REGISTRY.validate_event(self.decoded_data, event_name, version, raise_error=False)

    def get_type(self) -> str:
        event_name = self.decoded_data.get("event_name")
        version = self.decoded_data.get("event_version")
        return f"{event_name}-v{version}"

    def get_time(self) -> dt.datetime:
        return self.decoded_data.get("event_time")

    def get_data(self) -> dict:
        return self.decoded_data


class BaseConsumer(BaseSubscriber, abc.ABC):
    router: ty.Dict[str, str] = {}

    def _should_process_message(self, message: Message):
        if not message.valid:
            logger.warning(f"Invalid {message=}")
            return False
        return True

    def _handle(self, message: Message):
        event_name = message.data.get("event_name")
        method_name = self.router.get(event_name)
        if not method_name:
            raise ErrorMessageReceiverProcess(f"Unknown {event_name=}")
        method = getattr(self, method_name, None)
        if not method:
            raise ErrorMessageReceiverProcess(f"Programming error: {self.__class__} hasn't {method_name=}")
        method(message)
