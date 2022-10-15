from django.utils import timezone
from dynamic_rest.viewsets import DynamicModelViewSet
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api.permissions import IsAdminRole, IsManagerRole
from apps.api.serializers.tasks import TaskSerializer
from apps.tasks.models import Task
from apps.users.models import User


class TaskViewSet(DynamicModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    http_method_names = ["get", "post", "patch", "options"]

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset(queryset)
        if self.request.user.role not in [User.ROLE_ADMIN, User.ROLE_MANAGER]:
            queryset = queryset.filter(executor=self.request.user)
        return queryset


@api_view(http_method_names=["post"])
@permission_classes([IsAuthenticated, IsAdminRole | IsManagerRole])
def reassign_tasks(request):
    available_users = User.objects.filter(role=User.ROLE_POPUG).values_list("id", flat=True)
    tasks = list(Task.objects.filter(status=Task.STATUS_IN_PROGRESS))
    now = timezone.now()
    for t in tasks:
        t.set_random_user(available_users)
        t.updated_at = now
    Task.objects.bulk_update(tasks, fields=["executor", "updated_at"])
    return Response({"count": len(tasks)}, status=status.HTTP_200_OK)
