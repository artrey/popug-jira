import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.backends import TokenBackend as BaseTokenBackend
from rest_framework_simplejwt.exceptions import TokenBackendError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken as BaseAccessToken


class TokenBackend(BaseTokenBackend):
    AUTH_SERVER_VERIFY_ENDPOINT = settings.AUTH_SERVER_VERIFY_ENDPOINT

    def decode(self, token, verify=True):
        if verify:
            response = requests.post(self.AUTH_SERVER_VERIFY_ENDPOINT, {"token": token})
            if not response.ok:
                raise TokenBackendError(_("Token is invalid or expired"))
        return super().decode(token, verify=False)


class AccessToken(BaseAccessToken):
    _token_backend = TokenBackend(
        api_settings.ALGORITHM,
        api_settings.SIGNING_KEY,
        api_settings.VERIFYING_KEY,
        api_settings.AUDIENCE,
        api_settings.ISSUER,
        api_settings.JWK_URL,
        api_settings.LEEWAY,
        api_settings.JSON_ENCODER,
    )
