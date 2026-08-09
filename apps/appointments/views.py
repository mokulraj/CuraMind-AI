from rest_framework.viewsets import ModelViewSet

from .models import Appointment

from .permissions import (
    CanManageAppointments,
    IsAppointmentParticipant,
)

from .serializers import (
    AppointmentSerializer,
)


class AppointmentViewSet(ModelViewSet):
    """
    Appointment API.

    Patients can access their own appointments.
    Doctors and authorized staff can manage appointments.
    """

    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user

        queryset = (
            Appointment.objects
            .select_related(
                "patient",
                "doctor",
            )
            .all()
            .order_by("-scheduled_start")
        )

        if not user.is_authenticated:
            return queryset.none()

        if user.is_superuser:
            return queryset

        role = getattr(
            user,
            "role",
            None,
        )

        if role == "PATIENT":
            patient = getattr(
                user,
                "patient_profile",
                None,
            )

            if patient:
                return queryset.filter(
                    patient=patient
                )

            return queryset.none()

        if role == "DOCTOR":
            doctor = getattr(
                user,
                "doctor_profile",
                None,
            )

            if doctor:
                return queryset.filter(
                    doctor=doctor
                )

            return queryset.none()

        if role in {
            "STAFF",
            "NURSE",
            "RECEPTIONIST",
            "ADMIN",
        }:
            return queryset

        return queryset.none()

    def get_permissions(self):
        if self.action in {
            "create",
            "update",
            "partial_update",
            "destroy",
        }:
            permission_classes = [
                CanManageAppointments
            ]
        else:
            permission_classes = [
                CanManageAppointments,
                IsAppointmentParticipant,
            ]

        return [
            permission()
            for permission in permission_classes
        ]