# permissions.py

from rest_framework import permissions

class IsAdminOrSameUser(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the object or admin users.
        return obj == request.user or request.user.is_staff