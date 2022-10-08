from dynamic_rest.serializers import DynamicModelSerializer

from apps.users.models import User


class UserSerializer(DynamicModelSerializer):
    class Meta:
        model = User
        fields = ["id", "public_id", "role", "username", "first_name", "last_name"]
