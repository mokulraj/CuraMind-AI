from rest_framework.permissions import BasePermission


class CanAccessClinicalReports(BasePermission):
    """
    Access to clinical reports.
    """

    message = "You do not have clinical report access."

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


class CanCreateClinicalReport(BasePermission):
    """
    Only authorized clinical professionals may create
    clinical reports.
    """

    message = "Clinical report creation access is required."

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
                    "ADMIN",
                }
            )
        )


class CanSignClinicalReport(BasePermission):
    """
    Report signing is restricted to authorized clinicians.
    """

    message = "Clinical report signing access is required."

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
                }
            )
        )