from projects.models import ProjectMember
from rest_framework import permissions


class IsOwnerOrProjectAdmin(permissions.BasePermission):
    """
    Allow only the project owner, a project admin, or superuser to modify or delete.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Superuser has all permissions
        if user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, "owner") and obj.owner == user:
            return True

        return ProjectMember.objects.filter(
            project=obj, user=user, role="admin"
        ).exists()
