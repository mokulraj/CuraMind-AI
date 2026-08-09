import uuid
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel, Department, Organization
from apps.users.models import DoctorProfile, PatientProfile


class AppointmentStatus(models.TextChoices):
    SCHEDULED = "SCHEDULED", "Scheduled"
    CONFIRMED = "CONFIRMED", "Confirmed"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"
    NO_SHOW = "NO_SHOW", "No Show"
    RESCHEDULED = "RESCHEDULED", "Rescheduled"


class AppointmentType(models.TextChoices):
    INITIAL = "INITIAL", "Initial Consultation"
    FOLLOW_UP = "FOLLOW_UP", "Follow-up"
    ROUTINE = "ROUTINE", "Routine Check-up"
    EMERGENCY = "EMERGENCY", "Emergency"
    SPECIALIST = "SPECIALIST", "Specialist Consultation"
    REVIEW = "REVIEW", "Report Review"


class ConsultationMode(models.TextChoices):
    IN_PERSON = "IN_PERSON", "In Person"
    VIDEO = "VIDEO", "Video Consultation"
    AUDIO = "AUDIO", "Audio Consultation"


class Appointment(BaseModel):
    """
    Represents a scheduled healthcare appointment between
    a patient and a doctor.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    appointment_number = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        editable=False,
    )

    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.PROTECT,
        related_name="appointments",
    )

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        related_name="appointments",
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="appointments",
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="appointments",
    )

    appointment_type = models.CharField(
        max_length=30,
        choices=AppointmentType.choices,
        default=AppointmentType.INITIAL,
        db_index=True,
    )

    consultation_mode = models.CharField(
        max_length=20,
        choices=ConsultationMode.choices,
        default=ConsultationMode.IN_PERSON,
    )

    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.SCHEDULED,
        db_index=True,
    )

    scheduled_start = models.DateTimeField(
        db_index=True,
    )

    scheduled_end = models.DateTimeField(
        db_index=True,
    )

    reason = models.TextField(
        blank=True,
    )

    symptoms = models.TextField(
        blank=True,
    )

    doctor_notes = models.TextField(
        blank=True,
    )

    cancellation_reason = models.TextField(
        blank=True,
    )

    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "appointments"
        ordering = ["scheduled_start"]
        indexes = [
            models.Index(
                fields=[
                    "doctor",
                    "scheduled_start",
                    "status",
                ],
                name="appt_doctor_schedule_idx",
            ),
            models.Index(
                fields=[
                    "patient",
                    "scheduled_start",
                ],
                name="appt_patient_schedule_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "scheduled_start",
                ],
                name="appt_org_schedule_idx",
            ),
            models.Index(
                fields=[
                    "status",
                    "scheduled_start",
                ],
                name="appt_status_schedule_idx",
            ),
        ]

    def clean(self):
        """
        Validate appointment scheduling rules.
        """

        if self.scheduled_end <= self.scheduled_start:
            raise ValidationError(
                "Appointment end time must be after start time."
            )

        if self.scheduled_start < timezone.now():
            if self._state.adding:
                raise ValidationError(
                    "A new appointment cannot be scheduled in the past."
                )

        if self.department.organization_id != self.organization_id:
            raise ValidationError(
                "The selected department must belong to the organization."
            )

        if (
            self.doctor.user.role != "DOCTOR"
        ):
            raise ValidationError(
                "The selected user is not registered as a doctor."
            )

        if self.patient.user.role != "PATIENT":
            raise ValidationError(
                "The selected user is not registered as a patient."
            )

    def save(self, *args, **kwargs):
        if not self.appointment_number:
            self.appointment_number = (
                f"APT-{uuid.uuid4().hex[:12].upper()}"
            )

        self.full_clean()

        super().save(*args, **kwargs)

    @property
    def duration_minutes(self):
        duration = self.scheduled_end - self.scheduled_start
        return int(duration.total_seconds() / 60)

    @property
    def is_upcoming(self):
        return (
            self.scheduled_start > timezone.now()
            and self.status
            in {
                AppointmentStatus.SCHEDULED,
                AppointmentStatus.CONFIRMED,
            }
        )

    def __str__(self):
        return self.appointment_number


class DoctorAvailability(BaseModel):
    """
    Defines recurring availability for a doctor.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name="availability_slots",
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="doctor_availability",
    )

    weekday = models.PositiveSmallIntegerField(
        choices=[
            (0, "Monday"),
            (1, "Tuesday"),
            (2, "Wednesday"),
            (3, "Thursday"),
            (4, "Friday"),
            (5, "Saturday"),
            (6, "Sunday"),
        ],
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    slot_duration_minutes = models.PositiveSmallIntegerField(
        default=30,
    )

    break_duration_minutes = models.PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        db_table = "doctor_availability"
        ordering = [
            "weekday",
            "start_time",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "doctor",
                    "weekday",
                    "start_time",
                    "end_time",
                ],
                name="unique_doctor_availability",
            ),
        ]
        indexes = [
            models.Index(
                fields=[
                    "doctor",
                    "weekday",
                    "is_active",
                ],
                name="doctor_weekday_active_idx",
            ),
        ]

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError(
                "Availability end time must be after start time."
            )

        if self.slot_duration_minutes <= 0:
            raise ValidationError(
                "Slot duration must be greater than zero."
            )

        if self.organization_id != self.doctor.user.id:
            # Organization membership is validated later when
            # organization/staff membership is introduced.
            pass

    def __str__(self):
        return (
            f"{self.doctor.user.full_name} - "
            f"{self.get_weekday_display()}"
        )


class AppointmentNote(BaseModel):
    """
    Clinical or administrative note associated with an appointment.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name="notes",
    )

    author = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="appointment_notes",
    )

    note = models.TextField()

    is_clinical = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "appointment_notes"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "appointment",
                    "created_at",
                ],
                name="appt_note_created_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.appointment.appointment_number} - "
            f"{self.author.email}"
        )