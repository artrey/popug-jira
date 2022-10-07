import logging
import traceback

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import set_rollback

logger = logging.getLogger(__name__)


def exception_handler(exc, context):  # noqa: C901
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()
    elif not isinstance(exc, exceptions.APIException):
        logger.exception(exc)
        exc = exceptions.APIException(detail=str(exc).split("\n"), code="unexpected-error")

    headers = {}
    if getattr(exc, "auth_header", None):
        headers["WWW-Authenticate"] = exc.auth_header
    if getattr(exc, "wait", None):
        headers["Retry-After"] = "%d" % exc.wait

    details = exc.get_full_details()
    if isinstance(details, list) and len(details) == 1:
        data = {"detail": details[0]}
    elif isinstance(details, dict) and "code" in details:
        data = {"detail": details}
    elif isinstance(details, dict) and len(details) == 1 and "code" in next(iter(details.values()))[0]:
        data = {"detail": next(iter(details.values()))[0]}
    else:
        data = {"detail": {"message": "Complex error", "code": "complex-error"}, "details": details}

    if settings.DEBUG and exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        data["traceback"] = traceback.format_exc().split("\n")

    set_rollback()
    return Response(data, status=exc.status_code, headers=headers)
