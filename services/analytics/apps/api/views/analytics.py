import datetime as dt
import typing as ty

from django.db.models import Max, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import Account
from apps.analytics.models import TaskEvent
from apps.api.permissions import IsAdminRole


def _parse_since_to(request) -> ty.Tuple[dt.datetime, dt.datetime]:
    to = request.query_params.get("to")
    if not to:
        to = timezone.now()
    else:
        to = dt.datetime.fromisoformat(to)

    since = request.query_params.get("since")
    if not since:
        since = to - dt.timedelta(days=1)
    else:
        since = dt.datetime.fromisoformat(since)
    return since, to


@api_view(http_method_names=["get"])
@permission_classes([IsAuthenticated, IsAdminRole])
def company_earn(request):
    since, to = _parse_since_to(request)

    total_credit = TaskEvent.objects.filter(
        created_at__gte=since,
        created_at__lt=to,
        type=TaskEvent.EVENT_TYPE_ASSIGN,
    ).aggregate(total_credit=Coalesce(Sum("task__cost_assign"), 0))["total_credit"]

    total_debit = TaskEvent.objects.filter(
        created_at__gte=since,
        created_at__lt=to,
        type=TaskEvent.EVENT_TYPE_COMPLETE,
    ).aggregate(total_debit=Coalesce(Sum("task__cost_complete"), 0))["total_debit"]

    money = total_credit - total_debit

    return Response({"money": money})


@api_view(http_method_names=["get"])
@permission_classes([IsAuthenticated, IsAdminRole])
def most_expensive_task(request):
    since, to = _parse_since_to(request)

    max_cost = TaskEvent.objects.filter(
        created_at__gte=since,
        created_at__lt=to,
        task__completed=True,
        type=TaskEvent.EVENT_TYPE_COMPLETE,
    ).aggregate(max_cost=Coalesce(Max("task__cost_complete"), 0))["max_cost"]

    return Response({"max_cost": max_cost})


@api_view(http_method_names=["get"])
@permission_classes([IsAuthenticated, IsAdminRole])
def count_losers(request):
    count = Account.objects.filter(balance__lt=0).count()
    return Response({"count": count})
