from django.urls import include, path
from dynamic_rest.routers import DynamicRouter

from apps.api.views.accounts import AccountViewSet, TransactionViewSet, company_earn


class ApiRouter(DynamicRouter):
    include_root_view = False


router = ApiRouter()
router.register("accounts", AccountViewSet)
router.register("transactions", TransactionViewSet)

urlpatterns = [
    path("company-earn/", company_earn),
    path("", include(router.urls)),
]
