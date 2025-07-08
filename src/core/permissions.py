from rest_framework import permissions
from projects.models import ProjectMember


class IsOwnerOrProjectAdmin(permissions.BasePermission):
    """
    Allow only the project owner or a project admin to modify or delete.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user

        if hasattr(obj, "owner") and obj.owner == user:
            return True

        return ProjectMember.objects.filter(
            project=obj, user=user, role="admin"
        ).exists()
