from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    """
    Allows access only to superusers.
    """
    def has_permission(self, request, view):
        # Checks if user is logged in AND is a superuser
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)