from apps import kafka_util
from apps.users.models import User


def consume_user(message: dict):
    message = kafka_util.models.Message[kafka_util.models.User](**message)
    if message.event in ["create", "update"]:
        User.objects.update_or_create(public_id=message.public_id, defaults=message.data)
    elif message.event == "delete":
        User.objects.filter(public_id=message.public_id).delete()
