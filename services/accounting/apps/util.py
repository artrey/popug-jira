from kafka_util import producer

from accounting.celery import RetryableTask

send_event = RetryableTask(producer.send_event)
