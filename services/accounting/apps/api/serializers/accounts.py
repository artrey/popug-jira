from dynamic_rest.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer

from apps.accounts.models import Account, Transaction
from apps.api.serializers.users import UserSerializer


class AccountSerializer(DynamicModelSerializer):
    user = DynamicRelationField(UserSerializer, embed=True, deferred=True, read_only=True)
    transactions = DynamicRelationField("TransactionSerializer", many=True, embed=True, deferred=True, read_only=True)

    class Meta:
        model = Account
        fields = [
            "id",
            "public_id",
            "balance",
            "user",
            "transactions",
        ]
        read_only_fields = fields


class TransactionSerializer(DynamicModelSerializer):
    account = DynamicRelationField(AccountSerializer, embed=True, deferred=True, read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "public_id",
            "type",
            "description",
            "debit",
            "credit",
            "created_at",
            "account",
        ]
        read_only_fields = fields
