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
        """
        Create a new appointment after validating
        the scheduling rules.
        """

        # --------------------------------------------------
        # TIME VALIDATION
        # --------------------------------------------------

        if scheduled_start >= scheduled_end:
            raise ValueError(
                "Appointment start time must be before "
                "appointment end time."
            )

        if scheduled_start < timezone.now():
            raise ValueError(
                "Appointment cannot be scheduled in the past."
            )

        # --------------------------------------------------
        # DOCTOR DOUBLE-BOOKING CHECK
        # --------------------------------------------------

        overlapping = (
            Appointment.objects
            .filter(
                doctor=doctor,
                scheduled_start__lt=scheduled_end,
                scheduled_end__gt=scheduled_start,
            )
            .exclude(
                status=AppointmentStatus.CANCELLED,
            )
        )

        if overlapping.exists():
            raise ValueError(
                "Doctor already has an appointment "
                "during this time."
            )

        # --------------------------------------------------
        # CREATE APPOINTMENT
        # --------------------------------------------------

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
        """
        Cancel an existing appointment.
        """

        if appointment.status in {
            AppointmentStatus.COMPLETED,
            AppointmentStatus.CANCELLED,
        }:
            raise ValueError(
                "This appointment cannot be cancelled."
            )

        appointment.status = (
            AppointmentStatus.CANCELLED
        )

        appointment.cancellation_reason = reason

        appointment.save(
            update_fields=[
                "status",
                "cancellation_reason",
                "updated_at",
            ]
        )

        return appointment

    @staticmethod
    @transaction.atomic
    def confirm_appointment(
        *,
        appointment,
    ):
        """
        Confirm a scheduled appointment.
        """

        if appointment.status != AppointmentStatus.SCHEDULED:
            raise ValueError(
                "Only scheduled appointments can be confirmed."
            )

        if appointment.scheduled_start <= timezone.now():
            raise ValueError(
                "A past appointment cannot be confirmed."
            )

        appointment.status = (
            AppointmentStatus.CONFIRMED
        )

        appointment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return appointment

    @staticmethod
    @transaction.atomic
    def start_appointment(
        *,
        appointment,
    ):
        """
        Start an appointment.
        """

        if appointment.status != AppointmentStatus.CONFIRMED:
            raise ValueError(
                "Only confirmed appointments can be started."
            )

        appointment.status = (
            AppointmentStatus.IN_PROGRESS
        )

        appointment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return appointment

    @staticmethod
    @transaction.atomic
    def complete_appointment(
        *,
        appointment,
        doctor_notes="",
    ):
        """
        Complete an appointment and optionally
        save the doctor's clinical notes.
        """

        if appointment.status != AppointmentStatus.IN_PROGRESS:
            raise ValueError(
                "Only appointments in progress can be completed."
            )

        appointment.status = (
            AppointmentStatus.COMPLETED
        )

        appointment.doctor_notes = doctor_notes
        appointment.completed_at = timezone.now()

        appointment.save(
            update_fields=[
                "status",
                "doctor_notes",
                "completed_at",
                "updated_at",
            ]
        )

        return appointment