import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
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


@receiver(post_save, sender=User, dispatch_uid="user_streaming")
def send_comment_to_client(instance: User, **kwargs):
    kafka_util.send_message(
        "user-streaming",
        {
            param: str(getattr(instance, param)) if getattr(instance, param) else None
            for param in [
                "public_id",
                "username",
                "role",
                "first_name",
                "last_name",
            ]
        },
    )
