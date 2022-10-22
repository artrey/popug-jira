from dynamic_rest.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer

from apps.api.serializers.users import UserSerializer
from apps.tasks.models import Task


class TaskSerializer(DynamicModelSerializer):
    executor = DynamicRelationField(UserSerializer, embed=True, deferred=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "public_id",
            "jira_id",
            "title",
            "status",
            "executor",
            "cost_assign",
            "cost_complete",
        ]
        read_only_fields = fields
