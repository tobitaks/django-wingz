from rest_framework import permissions
from .models import User


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow users with role 'admin' to access the API.

    This checks the custom User model's role field instead of Django's
    built-in is_staff or is_superuser flags.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated and has admin role.
        """
        # User must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # For Django's built-in User (superuser), allow access
        if hasattr(request.user, 'is_superuser') and request.user.is_superuser:
            return True

        # Check if it's our custom User model with role='admin'
        try:
            # Try to get the custom User model instance
            custom_user = User.objects.filter(email=request.user.email).first()
            if custom_user and custom_user.role == 'admin':
                return True
        except Exception:
            pass

        return False
