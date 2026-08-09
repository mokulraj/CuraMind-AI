from rest_framework.permissions import BasePermission


class CanAccessMedicalRecord(BasePermission):
    """
    Clinical access to medical records.
    """

    message = "You do not have permission to access this medical record."

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
                    "NURSE",
                    "STAFF",
                    "ADMIN",
                }
            )
        )

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        user = request.user

        if user.is_superuser:
            return True

        patient = getattr(
            obj,
            "patient",
            None,
        )

        patient_user = getattr(
            patient,
            "user",
            None,
        )

        if patient_user == user:
            return True

        role = getattr(
            user,
            "role",
            None,
        )

        return role in {
            "DOCTOR",
            "NURSE",
            "STAFF",
            "ADMIN",
        }


class CanWriteClinicalData(BasePermission):
    """
    Only authorized clinical users may modify EMR data.
    """

    message = "Clinical write access is required."

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
                    "NURSE",
                    "ADMIN",
                }
            )
        )