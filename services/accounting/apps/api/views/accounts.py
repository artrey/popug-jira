import datetime as dt

from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from dynamic_rest.viewsets import DynamicModelViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import Account, Transaction
from apps.api.permissions import IsAdminRole, IsManagerRole
from apps.api.serializers.accounts import AccountSerializer, TransactionSerializer
from apps.users.models import User


class AccountViewSet(DynamicModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    http_method_names = ["get", "options"]
    permission_classes = [IsAuthenticated, IsAdminRole | IsManagerRole]

    @action(methods=["get"], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        instance = request.user.account
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TransactionViewSet(DynamicModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    http_method_names = ["get", "options"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self, queryset=None):
        qs = super().get_queryset(queryset)
        user = self.request.user
        if user.role not in [User.ROLE_ADMIN, User.ROLE_MANAGER]:
            qs = qs.filter(account=user.account)
        return qs


@api_view(http_method_names=["get"])
@permission_classes([IsAuthenticated, IsAdminRole | IsManagerRole])
def company_earn(request):
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

    total_sums = Transaction.objects.filter(created_at__gte=since, created_at__lt=to).aggregate(
        total_debit=Coalesce(Sum("debit"), 0),
        total_credit=Coalesce(Sum("credit"), 0),
    )
    money = total_sums["total_credit"] - total_sums["total_debit"]

    return Response({"money": money})
