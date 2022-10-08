import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps import kafka_util


class User(AbstractUser):
    class Meta:
        db_table = "users"

    ROLE_ADMIN = "Администратор"
    ROLE_MANAGER = "Менеджер"
    ROLE_ACCOUNTANT = "Бухгалтер"
    ROLE_POPUG = "Попуг"
    ROLES = (
        ROLE_ADMIN,
        ROLE_MANAGER,
        ROLE_ACCOUNTANT,
        ROLE_POPUG,
    )

    public_id = models.UUIDField(default=uuid.uuid4, unique=True)
    role = models.CharField(max_length=20, choices=[(x, x) for x in ROLES], default=ROLE_POPUG)

    def __str__(self):
        name = self.get_full_name()
        if name:
            return f"{self.username} ({name})"
        return self.username


@receiver(post_save, sender=User, dispatch_uid="user_streaming_create_update")
def user_streaming_create_update(instance: User, created: bool, **kwargs):
    kafka_util.send_message(
        "user-streaming",
        kafka_util.models.Message(
            entity="user",
            event="create" if created else "update",
            public_id=str(instance.public_id),
            data=kafka_util.models.User(
                **{
                    param: str(getattr(instance, param, ""))
                    for param in [
                        "username",
                        "role",
                        "first_name",
                        "last_name",
                    ]
                }
            ),
        ),
    )


@receiver(post_delete, sender=User, dispatch_uid="user_streaming_delete")
def user_streaming_delete(instance: User, **kwargs):
    kafka_util.send_message(
        "user-streaming",
        kafka_util.models.Message(
            entity="user",
            event="delete",
            public_id=str(instance.public_id),
            data=None,
        ),
    )
