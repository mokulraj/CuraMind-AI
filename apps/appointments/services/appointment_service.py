from django.db import transaction
from django.utils import timezone

from apps.appointments.models import (
    Appointment,
    AppointmentStatus,
)


class AppointmentService:
    """
    Business operations for appointments.
    """

    @staticmethod
    @transaction.atomic
    def create_appointment(
        *,
        patient,
        doctor,
        scheduled_start,
        scheduled_end,
        **extra_fields,
    ):
        if scheduled_start >= scheduled_end:
            raise ValueError(
                "Appointment start time must be before "
                "appointment end time."
            )

        if scheduled_start < timezone.now():
            raise ValueError(
                "Appointment cannot be scheduled in the past."
            )

        overlapping = Appointment.objects.filter(
            doctor=doctor,
            scheduled_start__lt=scheduled_end,
            scheduled_end__gt=scheduled_start,
        ).exclude(
            status__in=[
                AppointmentStatus.CANCELLED,
                AppointmentStatus.REJECTED,
            ]
        )

        if overlapping.exists():
            raise ValueError(
                "Doctor already has an appointment "
                "during this time."
            )

        return Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            **extra_fields,
        )

    @staticmethod
    @transaction.atomic
    def cancel_appointment(
        *,
        appointment,
        reason="",
    ):
        if appointment.status in {
            AppointmentStatus.COMPLETED,
            AppointmentStatus.CANCELLED,
        }:
            raise ValueError(
                "This appointment cannot be cancelled."
            )

        appointment.status = AppointmentStatus.CANCELLED

        if hasattr(appointment, "cancellation_reason"):
            appointment.cancellation_reason = reason

        update_fields = [
            "status",
            "updated_at",
        ]

        if hasattr(appointment, "cancellation_reason"):
            update_fields.append("cancellation_reason")

        appointment.save(
            update_fields=update_fields
        )

        return appointment