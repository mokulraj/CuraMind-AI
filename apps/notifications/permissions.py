from rest_framework.permissions import BasePermission


class IsNotificationOwner(BasePermission):
    """
    Users can access their own notifications.
    """

    message = "You can only access your own notifications."

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return (
            user.is_superuser
            or getattr(obj, "user_id", None)
            == user.id
        )


class CanManageNotifications(BasePermission):
    """
    Allows authorized staff to manage notifications.
    """

    message = "Notification management access is required."

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
                    "STAFF",
                    "RECEPTIONIST",
                }
            )
        )