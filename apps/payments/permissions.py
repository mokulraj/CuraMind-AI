from rest_framework.permissions import BasePermission


class CanViewPayment(BasePermission):
    """
    Patients can view their own payments.
    Authorized staff can view payment records.
    """

    message = "You do not have payment access."

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
                    "ADMIN",
                    "STAFF",
                    "RECEPTIONIST",
                }
            )
        )


class CanManagePayment(BasePermission):
    """
    Payment operations are restricted to authorized users.
    """

    message = "Payment management access is required."

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
                    "FINANCE",
                }
            )
        )


class IsPaymentOwner(BasePermission):
    """
    Object-level payment ownership.
    """

    message = "You can only access your own payment."

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        user = request.user

        if not user or not user.is_authenticated:
            return False

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

        return patient_user == user