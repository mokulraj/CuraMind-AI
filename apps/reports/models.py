import uuid

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel
from apps.emr.models import ClinicalEncounter, MedicalRecord
from apps.imaging.models import ImagingStudy
from apps.users.models import DoctorProfile, PatientProfile, User


class ReportType(models.TextChoices):
    CLINICAL = "CLINICAL", "Clinical Report"
    DISCHARGE = "DISCHARGE", "Discharge Report"
    CONSULTATION = "CONSULTATION", "Consultation Report"
    LABORATORY = "LABORATORY", "Laboratory Report"
    RADIOLOGY = "RADIOLOGY", "Radiology Report"
    PATHOLOGY = "PATHOLOGY", "Pathology Report"
    AI_ANALYSIS = "AI_ANALYSIS", "AI Analysis Report"
    MEDICAL_SUMMARY = "MEDICAL_SUMMARY", "Medical Summary"
    OTHER = "OTHER", "Other"


class ReportStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    IN_REVIEW = "IN_REVIEW", "In Review"
    APPROVED = "APPROVED", "Approved"
    FINAL = "FINAL", "Final"
    AMENDED = "AMENDED", "Amended"
    CANCELLED = "CANCELLED", "Cancelled"


class ReportFormat(models.TextChoices):
    HTML = "HTML", "HTML"
    PDF = "PDF", "PDF"
    DOCX = "DOCX", "DOCX"
    JSON = "JSON", "JSON"


class ReportTemplate(BaseModel):
    """
    Reusable template for generating healthcare reports.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=200,
        unique=True,
        db_index=True,
    )

    report_type = models.CharField(
        max_length=30,
        choices=ReportType.choices,
        db_index=True,
    )

    description = models.TextField(
        blank=True,
    )

    template_content = models.TextField()

    schema = models.JSONField(
        default=dict,
        blank=True,
    )

    version = models.PositiveIntegerField(
        default=1,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="report_templates_created",
    )

    class Meta:
        db_table = "report_templates"
        ordering = ["name"]
        indexes = [
            models.Index(
                fields=[
                    "report_type",
                    "is_active",
                ],
                name="report_template_type_idx",
            ),
        ]

    def __str__(self):
        return self.name


class ClinicalReport(BaseModel):
    """
    Primary report entity.

    A report may be connected to a clinical encounter, medical
    record, imaging study, or multiple clinical contexts.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    report_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        editable=False,
    )

    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.PROTECT,
        related_name="clinical_reports",
    )

    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.PROTECT,
        related_name="clinical_reports",
    )

    encounter = models.ForeignKey(
        ClinicalEncounter,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="reports",
    )

    imaging_study = models.ForeignKey(
        ImagingStudy,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="generated_reports",
    )

    report_type = models.CharField(
        max_length=30,
        choices=ReportType.choices,
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=ReportStatus.choices,
        default=ReportStatus.DRAFT,
        db_index=True,
    )

    title = models.CharField(
        max_length=255,
    )

    summary = models.TextField(
        blank=True,
    )

    content = models.TextField(
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

    template = models.ForeignKey(
        ReportTemplate,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="reports",
    )

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="reports_authored",
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="reports_reviewed",
    )

    signed_by = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="reports_signed",
    )

    generated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    signed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "clinical_reports"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "patient",
                    "created_at",
                ],
                name="report_patient_date_idx",
            ),
            models.Index(
                fields=[
                    "medical_record",
                    "report_type",
                ],
                name="report_record_type_idx",
            ),
            models.Index(
                fields=[
                    "status",
                    "report_type",
                ],
                name="report_status_type_idx",
            ),
            models.Index(
                fields=[
                    "author",
                    "created_at",
                ],
                name="report_author_date_idx",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.report_number:
            self.report_number = (
                f"RPT-{uuid.uuid4().hex[:12].upper()}"
            )

        self.full_clean()

        super().save(*args, **kwargs)

    def clean(self):
        if self.medical_record.patient_id != self.patient_id:
            raise ValidationError(
                "Medical record and report patient must match."
            )

        if self.encounter:
            if self.encounter.patient_id != self.patient_id:
                raise ValidationError(
                    "Encounter and report patient must match."
                )

        if self.imaging_study:
            if self.imaging_study.patient_id != self.patient_id:
                raise ValidationError(
                    "Imaging study and report patient must match."
                )

        if self.status in {
            ReportStatus.APPROVED,
            ReportStatus.FINAL,
            ReportStatus.AMENDED,
        } and not self.reviewer:
            raise ValidationError(
                "Approved or final reports require a reviewer."
            )

        if self.status in {
            ReportStatus.FINAL,
            ReportStatus.AMENDED,
        } and not self.signed_by:
            raise ValidationError(
                "Final reports require a signing doctor."
            )

    def __str__(self):
        return self.report_number


class ReportVersion(BaseModel):
    """
    Immutable-style version history for a clinical report.

    Every meaningful report revision gets its own version.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    report = models.ForeignKey(
        ClinicalReport,
        on_delete=models.PROTECT,
        related_name="versions",
    )

    version_number = models.PositiveIntegerField()

    title = models.CharField(
        max_length=255,
    )

    content = models.TextField(
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

    changed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="report_versions_created",
    )

    change_reason = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "report_versions"
        ordering = [
            "report",
            "-version_number",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "report",
                    "version_number",
                ],
                name="unique_report_version",
            ),
        ]
        indexes = [
            models.Index(
                fields=[
                    "report",
                    "version_number",
                ],
                name="report_version_lookup_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.report.report_number} "
            f"v{self.version_number}"
        )


class GeneratedReport(BaseModel):
    """
    Represents a generated report artifact.

    Binary files are stored in object storage. This table stores
    metadata and the secure storage reference.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    report = models.ForeignKey(
        ClinicalReport,
        on_delete=models.PROTECT,
        related_name="generated_artifacts",
    )

    format = models.CharField(
        max_length=10,
        choices=ReportFormat.choices,
    )

    storage_key = models.CharField(
        max_length=1024,
        unique=True,
    )

    file_name = models.CharField(
        max_length=500,
    )

    content_type = models.CharField(
        max_length=150,
    )

    file_size_bytes = models.PositiveBigIntegerField(
        default=0,
    )

    checksum_sha256 = models.CharField(
        max_length=64,
        blank=True,
    )

    generated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="generated_reports",
    )

    generated_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "generated_reports"
        ordering = ["-generated_at"]
        indexes = [
            models.Index(
                fields=[
                    "report",
                    "format",
                ],
                name="generated_report_lookup_idx",
            ),
        ]

    def __str__(self):
        return self.file_name


class ReportExportStatus(models.TextChoices):
    REQUESTED = "REQUESTED", "Requested"
    PROCESSING = "PROCESSING", "Processing"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"
    CANCELLED = "CANCELLED", "Cancelled"


class ReportExport(BaseModel):
    """
    Tracks asynchronous report export jobs.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    report = models.ForeignKey(
        ClinicalReport,
        on_delete=models.PROTECT,
        related_name="exports",
    )

    requested_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="report_exports_requested",
    )

    format = models.CharField(
        max_length=10,
        choices=ReportFormat.choices,
        default=ReportFormat.PDF,
    )

    status = models.CharField(
        max_length=20,
        choices=ReportExportStatus.choices,
        default=ReportExportStatus.REQUESTED,
        db_index=True,
    )

    celery_task_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    storage_key = models.CharField(
        max_length=1024,
        blank=True,
    )

    failure_reason = models.TextField(
        blank=True,
    )

    requested_at = models.DateTimeField(
        auto_now_add=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "report_exports"
        ordering = ["-requested_at"]
        indexes = [
            models.Index(
                fields=[
                    "status",
                    "requested_at",
                ],
                name="report_export_status_idx",
            ),
            models.Index(
                fields=[
                    "requested_by",
                    "requested_at",
                ],
                name="report_export_user_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.report.report_number} - "
            f"{self.format}"
        )