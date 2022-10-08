import apps.kafka_util.proto as kafka_proto
from apps.users.models import User


def consume_user(message: dict):
    message = kafka_proto.Message[kafka_proto.User](**message)
    if message.event in ["create", "update"]:
        User.objects.update_or_create(public_id=message.public_id, defaults=message.data.dict())
    elif message.event == "delete":
        User.objects.filter(public_id=message.public_id).delete()
