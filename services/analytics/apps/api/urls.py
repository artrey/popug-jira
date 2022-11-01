from django.urls import include, path
from dynamic_rest.routers import DynamicRouter

from apps.api.views.analytics import company_earn, count_losers, most_expensive_task


class ApiRouter(DynamicRouter):
    include_root_view = False


router = ApiRouter()

urlpatterns = [
    path("company-earn/", company_earn),
    path("count-losers/", count_losers),
    path("most-expensive-task/", most_expensive_task),
    path("", include(router.urls)),
]
