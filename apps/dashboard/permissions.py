from rest_framework.permissions import BasePermission


class CanAccessDashboard(BasePermission):
    """
    Authenticated active users may access dashboards.
    """

    message = "Dashboard access is required."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.is_active
        )


class CanManageDashboard(BasePermission):
    """
    Administrative dashboard configuration.
    """

    message = "Dashboard administration access is required."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return (
            user.is_active
            and (
                user.is_superuser
                or getattr(user, "role", None)
                in {
                    "ADMIN",
                    "ORGANIZATION_ADMIN",
                }
            )
        )