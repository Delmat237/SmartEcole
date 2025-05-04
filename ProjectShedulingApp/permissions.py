# ProjectShedulingApp/permissions.py
from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Seuls les admins peuvent modifier. Les autres peuvent juste lire.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'teacher')