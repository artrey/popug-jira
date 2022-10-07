from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, token_refresh, token_verify

from apps.api.serializers.token import TokenObtainPairSerializer

token_urls = [
    path("", TokenObtainPairView.as_view(serializer_class=TokenObtainPairSerializer)),
    path("refresh/", token_refresh),
    path("verify/", token_verify),
]

urlpatterns = [
    path("token/", include(token_urls)),
]
