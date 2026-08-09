from rest_framework.permissions import BasePermission


class CanManageAppointments(BasePermission):
    """
    Doctors and healthcare staff can manage appointments.
    """

    message = "You cannot manage appointments."

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
                    "STAFF",
                    "NURSE",
                    "RECEPTIONIST",
                    "ADMIN",
                }
            )
        )


class IsAppointmentParticipant(BasePermission):
    """
    Allows access to the patient or doctor participating
    in the appointment.
    """

    message = "You are not a participant in this appointment."

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

        patient = getattr(obj, "patient", None)
        doctor = getattr(obj, "doctor", None)

        patient_user = getattr(
            patient,
            "user",
            None,
        )

        doctor_user = getattr(
            doctor,
            "user",
            None,
        )

        return user in {
            patient_user,
            doctor_user,
        }