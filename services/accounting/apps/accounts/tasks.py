from accounting.celery import app
from apps.accounts.models import Account


@app.task
def daily_payouts():
    for account in Account.objects.all():
        account.create_transaction("payout", "daily payout", credit=account.balance)
        account.current_billing_cycle.close()
        # TODO: send email
