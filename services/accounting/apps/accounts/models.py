import uuid

from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.users.models import User
from apps.util import send_event


class Account(models.Model):
    class Meta:
        db_table = "accounts"

    public_id = models.UUIDField(default=uuid.uuid4, unique=True)
    balance = models.BigIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def current_billing_cycle(self) -> "BillingCycle":
        bc = self.billing_cycles.filter(closed=False).order_by("-start_date").first()
        if not bc:
            bc = BillingCycle.objects.create(account=self)
        return bc

    @transaction.atomic
    def create_transaction(
        self,
        type: str,
        description: str,
        debit: int = 0,
        credit: int = 0,
    ) -> "Transaction":
        t = Transaction.objects.create(
            account=self,
            billing_cycle=self.current_billing_cycle,
            type=type,
            description=description,
            debit=debit,
            credit=credit,
        )
        self.balance += t.debit - t.credit
        self.save(update_fields=["balance", "updated_at"])
        return t

    def __str__(self):
        return str(self.public_id)


class BillingCycle(models.Model):
    class Meta:
        db_table = "billing_cycles"

    public_id = models.UUIDField(default=uuid.uuid4, unique=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    closed = models.BooleanField(default=False, db_index=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="billing_cycles")

    def close(self):
        self.closed = True
        self.end_date = timezone.now()
        self.save(update_fields=["closed", "end_date"])

    def __str__(self):
        return str(self.public_id)


class Transaction(models.Model):
    class Meta:
        db_table = "transactions"

    public_id = models.UUIDField(default=uuid.uuid4, unique=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")
    billing_cycle = models.ForeignKey(BillingCycle, on_delete=models.CASCADE, related_name="transactions")
    type = models.CharField(max_length=100)
    description = models.TextField()
    debit = models.IntegerField(default=0)
    credit = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.public_id)


@receiver(post_save, sender=Account, dispatch_uid="transaction_create")
def transaction_create(instance: Account, created: bool, **kwargs):
    send_event(
        "account-stream",
        {param: str(getattr(instance, param, "")) for param in ["public_id", "balance"]}
        | {"owner_public_id": str(instance.user.public_id)},
        "accounting.AccountCreated" if created else "accounting.AccountUpdated",
        1,
        raise_error=True,
    )
