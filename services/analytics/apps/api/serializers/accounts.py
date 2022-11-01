from dynamic_rest.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer

from apps.accounts.models import Account
from apps.api.serializers.users import UserSerializer


class AccountSerializer(DynamicModelSerializer):
    user = DynamicRelationField(UserSerializer, embed=True, deferred=True, read_only=True)

    class Meta:
        model = Account
        fields = [
            "id",
            "public_id",
            "balance",
            "user",
            "created_at",
            "updated_at",
        ]
