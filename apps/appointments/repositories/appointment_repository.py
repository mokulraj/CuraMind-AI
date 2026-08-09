from django.db.models import Q

from apps.appointments.models import Appointment


class AppointmentRepository:
    """
    Database access for appointments.
    """

    @staticmethod
    def get_by_id(
        appointment_id,
    ):
        return (
            Appointment.objects
            .select_related(
                "patient",
                "doctor",
            )
            .filter(pk=appointment_id)
            .first()
        )

    @staticmethod
    def list_for_patient(
        patient_id,
    ):
        return (
            Appointment.objects
            .select_related(
                "patient",
                "doctor",
            )
            .filter(
                patient_id=patient_id
            )
            .order_by("-scheduled_start")
        )

    @staticmethod
    def list_for_doctor(
        doctor_id,
    ):
        return (
            Appointment.objects
            .select_related(
                "patient",
                "doctor",
            )
            .filter(
                doctor_id=doctor_id
            )
            .order_by("scheduled_start")
        )

    @staticmethod
    def find_overlapping(
        *,
        doctor_id,
        scheduled_start,
        scheduled_end,
        excluded_statuses=None,
    ):
        queryset = Appointment.objects.filter(
            doctor_id=doctor_id,
            scheduled_start__lt=scheduled_end,
            scheduled_end__gt=scheduled_start,
        )

        if excluded_statuses:
            queryset = queryset.exclude(
                status__in=excluded_statuses
            )

        return queryset

    @staticmethod
    def search(
        *,
        patient_id=None,
        doctor_id=None,
        status=None,
    ):
        queryset = Appointment.objects.select_related(
            "patient",
            "doctor",
        )

        if patient_id:
            queryset = queryset.filter(
                patient_id=patient_id
            )

        if doctor_id:
            queryset = queryset.filter(
                doctor_id=doctor_id
            )

        if status:
            queryset = queryset.filter(
                status=status
            )

        return queryset.order_by(
            "-scheduled_start"
        )