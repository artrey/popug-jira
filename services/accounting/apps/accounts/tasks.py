from django.core.mail import send_mail

from accounting.celery import app
from apps.accounts.models import Account


@app.task(autoretry_for=(Exception,), max_retries=3)
def daily_payouts():
    for account in Account.objects.all():
        transaction = None
        if account.balance > 0:
            transaction = account.create_transaction(
                "payout",
                "daily payout",
                credit=account.balance,
            )
        account.current_billing_cycle.close()

        if transaction:
            send_mail(
                "Daily payout",
                f"You earn ${transaction.credit}",
                "payout@popug.ai",
                [account.user.email],
                fail_silently=True,
            )
