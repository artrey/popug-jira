import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


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
