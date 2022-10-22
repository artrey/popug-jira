from rest_framework.permissions import BasePermission

from apps.users.models import User


class RolePermission(BasePermission):
    required_role = None

    def _check(self, request):
        return request.user.role == self.required_role

    def has_permission(self, request, view):
        return self._check(request)

    def has_object_permission(self, request, view, obj):
        return self._check(request)


class IsAdminRole(RolePermission):
    required_role = User.ROLE_ADMIN
