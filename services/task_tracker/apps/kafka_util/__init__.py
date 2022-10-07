import functools
import time
import typing as ty

from django.conf import settings
from django.utils.module_loading import import_string
from kafka import KafkaConsumer, KafkaProducer


def kafka_params(**override_params) -> dict:
    return {
        "bootstrap_servers": settings.KAFKA_SETTINGS.get("BOOTSTRAP_SERVERS"),
        "client_id": settings.KAFKA_SETTINGS.get("CLIENT_ID"),
        "value_serializer": import_string(settings.KAFKA_SETTINGS.get("VALUE_SERIALIZER")),
        "value_deserializer": import_string(settings.KAFKA_SETTINGS.get("VALUE_DESERIALIZER")),
    } | override_params


@functools.lru_cache(maxsize=None)
def default_kafka_producer() -> KafkaProducer:
    params = kafka_params()
    del params["value_deserializer"]
    return KafkaProducer(**params)


def send_message(topic: str, value: ty.Union[bytes, dict]):
    producer = default_kafka_producer()
    producer.send(topic, value)


def consume_forever(topic: str, action: ty.Callable[[dict], None]):
    params = kafka_params()
    del params["value_serializer"]
    consumer = KafkaConsumer(topic, **params, api_version=(0, 10))

    while True:
        for message in consumer:
            action(message.value)
        time.sleep(0.1)
