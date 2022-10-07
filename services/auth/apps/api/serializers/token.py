from rest_framework_simplejwt import serializers as base_serializers


class TokenObtainPairSerializer(base_serializers.TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        return token
