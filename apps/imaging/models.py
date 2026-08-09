import uuid

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel
from apps.emr.models import ClinicalEncounter, MedicalRecord
from apps.users.models import DoctorProfile, PatientProfile


class ImagingModality(models.TextChoices):
    XRAY = "XR", "X-Ray"
    CT = "CT", "Computed Tomography"
    MRI = "MR", "Magnetic Resonance Imaging"
    ULTRASOUND = "US", "Ultrasound"
    PET = "PT", "Positron Emission Tomography"
    MAMMOGRAPHY = "MG", "Mammography"
    FLUOROSCOPY = "RF", "Fluoroscopy"
    DEXA = "DX", "Bone Densitometry"
    OTHER = "OT", "Other"


class ImagingStudyStatus(models.TextChoices):
    ORDERED = "ORDERED", "Ordered"
    SCHEDULED = "SCHEDULED", "Scheduled"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"
    FAILED = "FAILED", "Failed"


class ImagingPriority(models.TextChoices):
    ROUTINE = "ROUTINE", "Routine"
    URGENT = "URGENT", "Urgent"
    STAT = "STAT", "Stat"


class ImagingStudy(BaseModel):
    """
    Represents a complete medical imaging study.

    One study may contain multiple DICOM series, and each series
    may contain multiple DICOM instances.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    study_instance_uid = models.CharField(
        max_length=128,
        unique=True,
        db_index=True,
    )

    accession_number = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
    )

    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.PROTECT,
        related_name="imaging_studies",
    )

    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.PROTECT,
        related_name="imaging_studies",
    )

    encounter = models.ForeignKey(
        ClinicalEncounter,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="imaging_studies",
    )

    ordered_by = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        related_name="imaging_studies_ordered",
    )

    modality = models.CharField(
        max_length=5,
        choices=ImagingModality.choices,
        db_index=True,
    )

    body_part = models.CharField(
        max_length=100,
    )

    study_description = models.CharField(
        max_length=500,
    )

    status = models.CharField(
        max_length=20,
        choices=ImagingStudyStatus.choices,
        default=ImagingStudyStatus.ORDERED,
        db_index=True,
    )

    priority = models.CharField(
        max_length=10,
        choices=ImagingPriority.choices,
        default=ImagingPriority.ROUTINE,
        db_index=True,
    )

    requested_at = models.DateTimeField()

    performed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    clinical_indication = models.TextField(
        blank=True,
    )

    clinical_history = models.TextField(
        blank=True,
    )

    referring_physician_notes = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "imaging_studies"
        ordering = ["-requested_at"]
        indexes = [
            models.Index(
                fields=[
                    "patient",
                    "requested_at",
                ],
                name="imaging_patient_date_idx",
            ),
            models.Index(
                fields=[
                    "modality",
                    "status",
                ],
                name="imaging_modality_status_idx",
            ),
            models.Index(
                fields=[
                    "status",
                    "priority",
                ],
                name="imaging_status_priority_idx",
            ),
        ]

    def clean(self):
        if self.medical_record.patient_id != self.patient_id:
            raise ValidationError(
                "The medical record does not belong to this patient."
            )

        if self.encounter:
            if self.encounter.patient_id != self.patient_id:
                raise ValidationError(
                    "The encounter does not belong to this patient."
                )

    def __str__(self):
        return (
            f"{self.accession_number} - "
            f"{self.get_modality_display()}"
        )


class ImagingSeries(BaseModel):
    """
    DICOM series belonging to an imaging study.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    series_instance_uid = models.CharField(
        max_length=128,
        unique=True,
        db_index=True,
    )

    study = models.ForeignKey(
        ImagingStudy,
        on_delete=models.PROTECT,
        related_name="series",
    )

    series_number = models.PositiveIntegerField()

    series_description = models.CharField(
        max_length=500,
        blank=True,
    )

    modality = models.CharField(
        max_length=5,
        choices=ImagingModality.choices,
    )

    body_part = models.CharField(
        max_length=100,
        blank=True,
    )

    number_of_instances = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        db_table = "imaging_series"
        ordering = ["series_number"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "study",
                    "series_number",
                ],
                name="unique_series_number_per_study",
            ),
        ]
        indexes = [
            models.Index(
                fields=[
                    "study",
                    "series_number",
                ],
                name="series_study_number_idx",
            ),
        ]

    def clean(self):
        if self.modality != self.study.modality:
            raise ValidationError(
                "Series modality must match the study modality."
            )

    def __str__(self):
        return (
            f"{self.study.accession_number} - "
            f"Series {self.series_number}"
        )


class DICOMInstance(BaseModel):
    """
    Represents an individual DICOM image instance.

    The actual file is referenced through object storage rather than
    storing binary DICOM content directly inside the relational DB.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    sop_instance_uid = models.CharField(
        max_length=128,
        unique=True,
        db_index=True,
    )

    series = models.ForeignKey(
        ImagingSeries,
        on_delete=models.PROTECT,
        related_name="instances",
    )

    instance_number = models.PositiveIntegerField()

    storage_key = models.CharField(
        max_length=1024,
        unique=True,
    )

    file_size_bytes = models.PositiveBigIntegerField(
        default=0,
    )

    checksum_sha256 = models.CharField(
        max_length=64,
        blank=True,
    )

    transfer_syntax_uid = models.CharField(
        max_length=128,
        blank=True,
    )

    sop_class_uid = models.CharField(
        max_length=128,
        blank=True,
    )

    rows = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    columns = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    bits_allocated = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    bits_stored = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    pixel_representation = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "dicom_instances"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "series",
                    "instance_number",
                ],
                name="unique_instance_per_series",
            ),
        ]
        indexes = [
            models.Index(
                fields=[
                    "series",
                    "instance_number",
                ],
                name="dicom_series_instance_idx",
            ),
        ]

    def __str__(self):
        return self.sop_instance_uid


class ReportStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PRELIMINARY = "PRELIMINARY", "Preliminary"
    FINAL = "FINAL", "Final"
    AMENDED = "AMENDED", "Amended"
    CANCELLED = "CANCELLED", "Cancelled"


class RadiologyReport(BaseModel):
    """
    Radiologist report associated with an imaging study.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    study = models.OneToOneField(
        ImagingStudy,
        on_delete=models.PROTECT,
        related_name="radiology_report",
    )

    radiologist = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        related_name="radiology_reports",
    )

    status = models.CharField(
        max_length=20,
        choices=ReportStatus.choices,
        default=ReportStatus.DRAFT,
        db_index=True,
    )

    clinical_history = models.TextField(
        blank=True,
    )

    findings = models.TextField(
        blank=True,
    )

    impression = models.TextField(
        blank=True,
    )

    recommendations = models.TextField(
        blank=True,
    )

    report_text = models.TextField(
        blank=True,
    )

    signed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "radiology_reports"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "radiologist",
                    "status",
                ],
                name="report_radiologist_status_idx",
            ),
        ]

    def clean(self):
        if self.study.status not in {
            ImagingStudyStatus.COMPLETED,
            ImagingStudyStatus.IN_PROGRESS,
        }:
            raise ValidationError(
                "A report can only be created for an active or "
                "completed imaging study."
            )

    def __str__(self):
        return (
            f"Report - "
            f"{self.study.accession_number}"
        )


class AIProcessingStatus(models.TextChoices):
    NOT_STARTED = "NOT_STARTED", "Not Started"
    QUEUED = "QUEUED", "Queued"
    PROCESSING = "PROCESSING", "Processing"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"


class ImagingAIProcessing(BaseModel):
    """
    Tracks an AI analysis job associated with an imaging study.

    The actual AI pipeline will be implemented in the AI Pipeline
    application in a later model step.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    study = models.ForeignKey(
        ImagingStudy,
        on_delete=models.PROTECT,
        related_name="ai_processing_jobs",
    )

    model_name = models.CharField(
        max_length=255,
    )

    model_version = models.CharField(
        max_length=100,
    )

    status = models.CharField(
        max_length=20,
        choices=AIProcessingStatus.choices,
        default=AIProcessingStatus.NOT_STARTED,
        db_index=True,
    )

    requested_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    error_message = models.TextField(
        blank=True,
    )

    result_storage_key = models.CharField(
        max_length=1024,
        blank=True,
    )

    confidence_score = models.DecimalField(
        max_digits=6,
        decimal_places=5,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "imaging_ai_processing"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "study",
                    "status",
                ],
                name="ai_study_status_idx",
            ),
            models.Index(
                fields=[
                    "model_name",
                    "model_version",
                ],
                name="ai_model_version_idx",
            ),
        ]

    def clean(self):
        if self.confidence_score is not None:
            if not 0 <= self.confidence_score <= 1:
                raise ValidationError(
                    "Confidence score must be between 0 and 1."
                )

    def __str__(self):
        return (
            f"{self.model_name} "
            f"{self.model_version} - "
            f"{self.study.accession_number}"
        )