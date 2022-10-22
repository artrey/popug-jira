from django.contrib import admin

from apps.accounts.models import Account, BillingCycle, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        "public_id",
        "balance",
        "user",
        "created_at",
        "updated_at",
    ]
    list_select_related = ["user"]
    search_fields = [
        "public_id",
        "user__username",
        "user__first_name",
        "user__last_name",
    ]


@admin.register(BillingCycle)
class BillingCycleAdmin(admin.ModelAdmin):
    list_display = [
        "public_id",
        "start_date",
        "end_date",
        "closed",
        "account",
    ]
    list_select_related = ["account"]
    list_filter = ["closed", "start_date", "end_date"]
    list_editable = ["closed"]
    search_fields = [
        "public_id",
        "account__public_id",
        "account__user__public_id",
    ]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "public_id",
        "account",
        "type",
        "description",
        "debit",
        "credit",
        "created_at",
    ]
    list_select_related = ["account"]
    search_fields = [
        "public_id",
        "type",
        "description",
        "account__public_id",
    ]
