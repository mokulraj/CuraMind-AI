import uuid

from django.core.exceptions import ValidationError
from django.db import models

from apps.appointments.models import Appointment
from apps.core.models import BaseModel
from apps.users.models import DoctorProfile, PatientProfile


class RecordStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    ARCHIVED = "ARCHIVED", "Archived"


class MedicalRecord(BaseModel):
    """
    Primary longitudinal medical record for a patient.

    A patient has one primary medical record. Individual clinical
    encounters, diagnoses, medications, allergies and observations
    are attached to this record.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    patient = models.OneToOneField(
        PatientProfile,
        on_delete=models.PROTECT,
        related_name="medical_record",
    )

    record_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        editable=False,
    )

    status = models.CharField(
        max_length=20,
        choices=RecordStatus.choices,
        default=RecordStatus.ACTIVE,
        db_index=True,
    )

    primary_physician = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="primary_medical_records",
    )

    summary = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "medical_records"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["status", "is_active"],
                name="emr_status_active_idx",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.record_number:
            self.record_number = (
                f"MRN-{uuid.uuid4().hex[:12].upper()}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.record_number


class EncounterType(models.TextChoices):
    OUTPATIENT = "OUTPATIENT", "Outpatient"
    INPATIENT = "INPATIENT", "Inpatient"
    EMERGENCY = "EMERGENCY", "Emergency"
    TELEMEDICINE = "TELEMEDICINE", "Telemedicine"
    FOLLOW_UP = "FOLLOW_UP", "Follow-up"


class EncounterStatus(models.TextChoices):
    OPEN = "OPEN", "Open"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"


class ClinicalEncounter(BaseModel):
    """
    Represents a clinical interaction with a patient.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.PROTECT,
        related_name="encounters",
    )

    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.PROTECT,
        related_name="clinical_encounters",
    )

    attending_doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        related_name="clinical_encounters",
    )

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="clinical_encounter",
    )

    encounter_type = models.CharField(
        max_length=20,
        choices=EncounterType.choices,
        default=EncounterType.OUTPATIENT,
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=EncounterStatus.choices,
        default=EncounterStatus.OPEN,
        db_index=True,
    )

    chief_complaint = models.TextField(
        blank=True,
    )

    history_of_present_illness = models.TextField(
        blank=True,
    )

    clinical_summary = models.TextField(
        blank=True,
    )

    examination_notes = models.TextField(
        blank=True,
    )

    treatment_plan = models.TextField(
        blank=True,
    )

    started_at = models.DateTimeField()

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "clinical_encounters"
        ordering = ["-started_at"]
        indexes = [
            models.Index(
                fields=[
                    "patient",
                    "started_at",
                ],
                name="encounter_patient_date_idx",
            ),
            models.Index(
                fields=[
                    "attending_doctor",
                    "started_at",
                ],
                name="encounter_doctor_date_idx",
            ),
            models.Index(
                fields=[
                    "status",
                    "started_at",
                ],
                name="encounter_status_date_idx",
            ),
        ]

    def clean(self):
        if self.medical_record.patient_id != self.patient_id:
            raise ValidationError(
                "The medical record does not belong to this patient."
            )

        if (
            self.appointment
            and self.appointment.patient_id != self.patient_id
        ):
            raise ValidationError(
                "The appointment does not belong to this patient."
            )

        if (
            self.appointment
            and self.appointment.doctor_id
            != self.attending_doctor_id
        ):
            raise ValidationError(
                "The appointment doctor and attending doctor must match."
            )

    def __str__(self):
        return (
            f"{self.patient.user.full_name} - "
            f"{self.get_encounter_type_display()}"
        )


class DiagnosisType(models.TextChoices):
    PRIMARY = "PRIMARY", "Primary"
    SECONDARY = "SECONDARY", "Secondary"
    DIFFERENTIAL = "DIFFERENTIAL", "Differential"
    HISTORICAL = "HISTORICAL", "Historical"


class DiagnosisStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    RESOLVED = "RESOLVED", "Resolved"
    INACTIVE = "INACTIVE", "Inactive"


class Diagnosis(BaseModel):
    """
    Diagnosis associated with a clinical encounter.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    encounter = models.ForeignKey(
        ClinicalEncounter,
        on_delete=models.PROTECT,
        related_name="diagnoses",
    )

    code = models.CharField(
        max_length=30,
        db_index=True,
    )

    description = models.CharField(
        max_length=500,
    )

    diagnosis_type = models.CharField(
        max_length=20,
        choices=DiagnosisType.choices,
        default=DiagnosisType.PRIMARY,
    )

    status = models.CharField(
        max_length=20,
        choices=DiagnosisStatus.choices,
        default=DiagnosisStatus.ACTIVE,
        db_index=True,
    )

    clinical_notes = models.TextField(
        blank=True,
    )

    diagnosed_by = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        related_name="diagnoses_created",
    )

    diagnosed_at = models.DateTimeField()

    class Meta:
        db_table = "diagnoses"
        indexes = [
            models.Index(
                fields=[
                    "encounter",
                    "diagnosis_type",
                ],
                name="diagnosis_enc_type_idx",
            ),
            models.Index(
                fields=[
                    "code",
                    "status",
                ],
                name="diagnosis_code_status_idx",
            ),
        ]

    def clean(self):
        if (
            self.diagnosed_by_id
            != self.encounter.attending_doctor_id
        ):
            raise ValidationError(
                "The diagnosing doctor must be the attending doctor."
            )

    def __str__(self):
        return f"{self.code} - {self.description}"


class AllergySeverity(models.TextChoices):
    MILD = "MILD", "Mild"
    MODERATE = "MODERATE", "Moderate"
    SEVERE = "SEVERE", "Severe"
    LIFE_THREATENING = (
        "LIFE_THREATENING",
        "Life Threatening",
    )


class AllergyStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    RESOLVED = "RESOLVED", "Resolved"


class Allergy(BaseModel):
    """
    Patient allergy information.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.PROTECT,
        related_name="allergies",
    )

    allergen = models.CharField(
        max_length=255,
        db_index=True,
    )

    reaction = models.TextField(
        blank=True,
    )

    severity = models.CharField(
        max_length=30,
        choices=AllergySeverity.choices,
        default=AllergySeverity.MILD,
    )

    status = models.CharField(
        max_length=20,
        choices=AllergyStatus.choices,
        default=AllergyStatus.ACTIVE,
        db_index=True,
    )

    notes = models.TextField(
        blank=True,
    )

    recorded_by = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        related_name="allergies_recorded",
    )

    class Meta:
        db_table = "allergies"
        indexes = [
            models.Index(
                fields=[
                    "medical_record",
                    "status",
                ],
                name="allergy_record_status_idx",
            ),
        ]

    def __str__(self):
        return self.allergen


class MedicationStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    COMPLETED = "COMPLETED", "Completed"
    DISCONTINUED = "DISCONTINUED", "Discontinued"


class Medication(BaseModel):
    """
    Medication prescribed to a patient.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.PROTECT,
        related_name="medications",
    )

    encounter = models.ForeignKey(
        ClinicalEncounter,
        on_delete=models.PROTECT,
        related_name="medications",
    )

    medication_name = models.CharField(
        max_length=255,
        db_index=True,
    )

    generic_name = models.CharField(
        max_length=255,
        blank=True,
    )

    dosage = models.CharField(
        max_length=100,
    )

    route = models.CharField(
        max_length=100,
    )

    frequency = models.CharField(
        max_length=100,
    )

    duration = models.CharField(
        max_length=100,
        blank=True,
    )

    instructions = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=MedicationStatus.choices,
        default=MedicationStatus.ACTIVE,
        db_index=True,
    )

    prescribed_by = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        related_name="medications_prescribed",
    )

    prescribed_at = models.DateTimeField()

    discontinued_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "medications"
        ordering = ["-prescribed_at"]
        indexes = [
            models.Index(
                fields=[
                    "medical_record",
                    "status",
                ],
                name="medication_record_status_idx",
            ),
            models.Index(
                fields=[
                    "medication_name",
                    "status",
                ],
                name="medication_name_status_idx",
            ),
        ]

    def clean(self):
        if self.medical_record.patient_id != (
            self.encounter.patient_id
        ):
            raise ValidationError(
                "Medication record and encounter patient must match."
            )

        if (
            self.prescribed_by_id
            != self.encounter.attending_doctor_id
        ):
            raise ValidationError(
                "The prescribing doctor must be the attending doctor."
            )

    def __str__(self):
        return self.medication_name


class VitalSign(BaseModel):
    """
    Vital signs recorded during a clinical encounter.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    encounter = models.ForeignKey(
        ClinicalEncounter,
        on_delete=models.PROTECT,
        related_name="vital_signs",
    )

    recorded_by = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="vital_signs_recorded",
    )

    temperature_celsius = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    heart_rate_bpm = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    respiratory_rate_bpm = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    systolic_bp_mmhg = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    diastolic_bp_mmhg = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    oxygen_saturation_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    weight_kg = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )

    height_cm = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )

    recorded_at = models.DateTimeField()

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "vital_signs"
        ordering = ["-recorded_at"]
        indexes = [
            models.Index(
                fields=[
                    "encounter",
                    "recorded_at",
                ],
                name="vitals_encounter_date_idx",
            ),
        ]

    def clean(self):
        if not any(
            [
                self.temperature_celsius is not None,
                self.heart_rate_bpm is not None,
                self.respiratory_rate_bpm is not None,
                self.systolic_bp_mmhg is not None,
                self.diastolic_bp_mmhg is not None,
                self.oxygen_saturation_percent is not None,
                self.weight_kg is not None,
                self.height_cm is not None,
            ]
        ):
            raise ValidationError(
                "At least one vital sign must be recorded."
            )

    def __str__(self):
        return (
            f"Vitals - "
            f"{self.encounter.patient.user.full_name}"
        )


class ClinicalNoteType(models.TextChoices):
    PROGRESS = "PROGRESS", "Progress Note"
    CONSULTATION = "CONSULTATION", "Consultation Note"
    DISCHARGE = "DISCHARGE", "Discharge Note"
    NURSING = "NURSING", "Nursing Note"
    OTHER = "OTHER", "Other"


class ClinicalNote(BaseModel):
    """
    Structured clinical documentation attached to an encounter.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    encounter = models.ForeignKey(
        ClinicalEncounter,
        on_delete=models.PROTECT,
        related_name="clinical_notes",
    )

    author = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="clinical_notes_authored",
    )

    note_type = models.CharField(
        max_length=30,
        choices=ClinicalNoteType.choices,
        default=ClinicalNoteType.PROGRESS,
    )

    content = models.TextField()

    signed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_signed = models.BooleanField(
        default=False,
        db_index=True,
    )

    class Meta:
        db_table = "clinical_notes"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "encounter",
                    "note_type",
                ],
                name="clinical_note_enc_type_idx",
            ),
            models.Index(
                fields=[
                    "author",
                    "created_at",
                ],
                name="clinical_note_author_idx",
            ),
        ]

    def clean(self):
        if self.is_signed and not self.signed_at:
            raise ValidationError(
                "A signed clinical note must have signed_at."
            )

        if not self.is_signed and self.signed_at:
            raise ValidationError(
                "An unsigned clinical note cannot have signed_at."
            )

    def __str__(self):
        return (
            f"{self.get_note_type_display()} - "
            f"{self.encounter.patient.user.full_name}"
        )