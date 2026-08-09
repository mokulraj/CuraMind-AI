from rest_framework.permissions import BasePermission


class CanReadAuditLogs(BasePermission):
    """
    Audit logs are available only to authorized administrators.
    """

    message = "Audit log access is restricted."

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
                    "SECURITY_ADMIN",
                }
            )
        )


class AuditReadOnly(BasePermission):
    """
    Explicitly blocks write operations against audit data.
    """

    message = "Audit records are read-only."

    def has_permission(self, request, view):
        return request.method in {
            "GET",
            "HEAD",
            "OPTIONS",
        }