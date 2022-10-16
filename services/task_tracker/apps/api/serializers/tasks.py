from dynamic_rest.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework.exceptions import ValidationError

from apps.api.serializers.users import UserSerializer
from apps.tasks.models import Task


class TaskSerializer(DynamicModelSerializer):
    executor = DynamicRelationField(UserSerializer, embed=True, deferred=True, read_only=True)

    class Meta:
        model = Task
        fields = ["id", "public_id", "jira_id", "title", "description", "status", "executor"]

    def validate_status(self, value):
        view = self.context["view"]
        if view.action == "create" and value != Task.STATUS_IN_PROGRESS:
            raise ValidationError("You cannot create completed task", code="prohibited-create-completed-task")
        return value

    def validate(self, attrs):
        view = self.context["view"]
        if view.action != "create" and view.get_object().status == Task.STATUS_COMPLETED:
            raise ValidationError("You cannot change completed task", code="prohibited-change-completed-task")
        return super().validate(attrs)
