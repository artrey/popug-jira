import uuid

from django.db import models

from apps.users.models import User


class Account(models.Model):
    class Meta:
        db_table = "accounts"

    public_id = models.UUIDField(default=uuid.uuid4, unique=True)
    balance = models.BigIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.public_id)
