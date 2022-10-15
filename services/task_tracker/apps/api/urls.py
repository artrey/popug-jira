from django.urls import include, path
from dynamic_rest.routers import DynamicRouter

from apps.api.views.tasks import TaskViewSet, reassign_tasks


class ApiRouter(DynamicRouter):
    include_root_view = False


router = ApiRouter()
router.register("tasks", TaskViewSet)

urlpatterns = [
    path("tasks/reassign/", reassign_tasks),
    path("", include(router.urls)),
]
