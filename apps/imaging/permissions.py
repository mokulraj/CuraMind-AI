from rest_framework.permissions import BasePermission


class CanAccessImaging(BasePermission):
    """
    Access to medical imaging data.
    """

    message = "You do not have imaging access."

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
                    "PATIENT",
                    "DOCTOR",
                    "RADIOLOGIST",
                    "NURSE",
                    "STAFF",
                    "ADMIN",
                }
            )
        )


class CanManageImaging(BasePermission):
    """
    Imaging management access.
    """

    message = "Imaging management access is required."

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
                    "DOCTOR",
                    "RADIOLOGIST",
                    "TECHNICIAN",
                    "ADMIN",
                }
            )
        )