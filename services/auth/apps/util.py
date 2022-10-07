import functools
import json

from django.conf import settings
from kafka import KafkaProducer


@functools.lru_cache(maxsize=None)
def _kafka_producer(bootstrap_servers: str, client_id: str) -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        client_id=client_id,
    )


def _send_to_kafka(
    topic: str,
    value: bytes,
    bootstrap_servers: str = settings.KAFKA_BOOTSTRAP_SERVERS,
    client_id: str = settings.KAFKA_CLIENT_ID,
):
    producer = _kafka_producer(bootstrap_servers=bootstrap_servers, client_id=client_id)
    producer.send(topic, value)


def _send_json_to_kafka(
    topic: str,
    value: bytes,
    bootstrap_servers: str = settings.KAFKA_BOOTSTRAP_SERVERS,
    client_id: str = settings.KAFKA_CLIENT_ID,
):
    producer = _kafka_producer(bootstrap_servers=bootstrap_servers, client_id=client_id)
    producer.send(topic, value)


def send_to_message_broker(topic: str, value: dict):
    payload = json.dumps(value).encode("utf-8")
    return _send_to_kafka(topic, payload)
