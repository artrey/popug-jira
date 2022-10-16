from django.contrib import admin

from apps.accounts.models import Account, Transaction


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
