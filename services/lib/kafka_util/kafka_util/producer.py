import datetime as dt
import functools
import logging
import typing as ty
import uuid

from django.conf import settings
from kafka import KafkaProducer

from kafka_util.serializers import json_serialize

logger = logging.getLogger(__name__)


def kafka_params(**override_params) -> dict:
    return {
        "bootstrap_servers": settings.KAFKA_HOSTS,
        "client_id": settings.KAFKA_CLIENT_ID,
    } | override_params


@functools.lru_cache(maxsize=None)
def default_kafka_producer() -> KafkaProducer:
    params = kafka_params()
    return KafkaProducer(**params)


def send_event(topic: str, value: ty.Optional[dict], event_name: str, version: int, raise_error: bool = False) -> bool:
    event_data = {
        "event_id": str(uuid.uuid4()),
        "event_name": event_name,
        "event_version": version,
        "event_time": dt.datetime.utcnow(),
        "producer": settings.KAFKA_CLIENT_ID,
        "data": value,
    }
    success = settings.SCHEME_REGISTRY.validate_event(event_data, event_name, version, raise_error)

    if success:
        producer = default_kafka_producer()
        blob = json_serialize(event_data)
        producer.send(topic, blob)
    else:
        logger.error(f"Invalid event: {event_data}")
    return success
