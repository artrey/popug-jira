from django.urls import include, path
from dynamic_rest.routers import DynamicRouter


class ApiRouter(DynamicRouter):
    include_root_view = False


router = ApiRouter()

urlpatterns = [
    path("", include(router.urls)),
]
