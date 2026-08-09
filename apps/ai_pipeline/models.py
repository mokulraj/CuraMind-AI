import uuid

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel
from apps.imaging.models import ImagingStudy
from apps.users.models import User


class AIModelType(models.TextChoices):
    CLASSIFICATION = "CLASSIFICATION", "Classification"
    DETECTION = "DETECTION", "Detection"
    SEGMENTATION = "SEGMENTATION", "Segmentation"
    PREDICTION = "PREDICTION", "Prediction"
    NLP = "NLP", "Natural Language Processing"
    MULTIMODAL = "MULTIMODAL", "Multimodal"


class AIModelFramework(models.TextChoices):
    PYTORCH = "PYTORCH", "PyTorch"
    TENSORFLOW = "TENSORFLOW", "TensorFlow"
    SKLEARN = "SKLEARN", "Scikit-learn"
    ONNX = "ONNX", "ONNX"
    HUGGINGFACE = "HUGGINGFACE", "Hugging Face"
    CUSTOM = "CUSTOM", "Custom"


class AIModelStatus(models.TextChoices):
    DEVELOPMENT = "DEVELOPMENT", "Development"
    VALIDATION = "VALIDATION", "Validation"
    PRODUCTION = "PRODUCTION", "Production"
    RETIRED = "RETIRED", "Retired"


class AIModel(BaseModel):
    """
    Registry entry for a healthcare AI model.

    The database stores model metadata. Actual model binaries are
    stored outside the relational database.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
    )

    display_name = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    model_type = models.CharField(
        max_length=30,
        choices=AIModelType.choices,
        db_index=True,
    )

    framework = models.CharField(
        max_length=30,
        choices=AIModelFramework.choices,
    )

    status = models.CharField(
        max_length=20,
        choices=AIModelStatus.choices,
        default=AIModelStatus.DEVELOPMENT,
        db_index=True,
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="ai_models_owned",
    )

    repository_url = models.URLField(
        blank=True,
    )

    documentation_url = models.URLField(
        blank=True,
    )

    license_name = models.CharField(
        max_length=255,
        blank=True,
    )

    is_clinical_use_approved = models.BooleanField(
        default=False,
        db_index=True,
    )

    class Meta:
        db_table = "ai_models"
        ordering = ["name"]
        indexes = [
            models.Index(
                fields=[
                    "model_type",
                    "status",
                ],
                name="ai_model_type_status_idx",
            ),
            models.Index(
                fields=[
                    "is_clinical_use_approved",
                    "status",
                ],
                name="ai_model_clinical_status_idx",
            ),
        ]

    def __str__(self):
        return self.display_name


class AIModelVersion(BaseModel):
    """
    Versioned release of an AI model.

    Every production inference should be traceable to an exact model
    version.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    model = models.ForeignKey(
        AIModel,
        on_delete=models.PROTECT,
        related_name="versions",
    )

    version = models.CharField(
        max_length=100,
    )

    artifact_storage_key = models.CharField(
        max_length=1024,
    )

    artifact_sha256 = models.CharField(
        max_length=64,
    )

    configuration_storage_key = models.CharField(
        max_length=1024,
        blank=True,
    )

    release_notes = models.TextField(
        blank=True,
    )

    input_schema_version = models.CharField(
        max_length=50,
        default="1.0",
    )

    output_schema_version = models.CharField(
        max_length=50,
        default="1.0",
    )

    accuracy = models.DecimalField(
        max_digits=7,
        decimal_places=5,
        null=True,
        blank=True,
    )

    sensitivity = models.DecimalField(
        max_digits=7,
        decimal_places=5,
        null=True,
        blank=True,
    )

    specificity = models.DecimalField(
        max_digits=7,
        decimal_places=5,
        null=True,
        blank=True,
    )

    auc = models.DecimalField(
        max_digits=7,
        decimal_places=5,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=False,
        db_index=True,
    )

    released_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "ai_model_versions"
        ordering = ["model", "-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "model",
                    "version",
                ],
                name="unique_ai_model_version",
            ),
        ]
        indexes = [
            models.Index(
                fields=[
                    "model",
                    "is_active",
                ],
                name="ai_version_active_idx",
            ),
        ]

    def clean(self):
        metrics = {
            "accuracy": self.accuracy,
            "sensitivity": self.sensitivity,
            "specificity": self.specificity,
            "auc": self.auc,
        }

        for name, value in metrics.items():
            if value is not None and not 0 <= value <= 1:
                raise ValidationError(
                    f"{name} must be between 0 and 1."
                )

    def __str__(self):
        return f"{self.model.name} v{self.version}"


class AIJobStatus(models.TextChoices):
    CREATED = "CREATED", "Created"
    QUEUED = "QUEUED", "Queued"
    PROCESSING = "PROCESSING", "Processing"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"
    CANCELLED = "CANCELLED", "Cancelled"


class AIJobPriority(models.TextChoices):
    LOW = "LOW", "Low"
    NORMAL = "NORMAL", "Normal"
    HIGH = "HIGH", "High"
    CRITICAL = "CRITICAL", "Critical"


class AIInferenceJob(BaseModel):
    """
    Represents one AI inference execution.

    A job is immutable from a clinical traceability perspective:
    model version, input and execution metadata are retained.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    job_reference = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        editable=False,
    )

    model_version = models.ForeignKey(
        AIModelVersion,
        on_delete=models.PROTECT,
        related_name="inference_jobs",
    )

    imaging_study = models.ForeignKey(
        ImagingStudy,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ai_inference_jobs",
    )

    requested_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="ai_jobs_requested",
    )

    status = models.CharField(
        max_length=20,
        choices=AIJobStatus.choices,
        default=AIJobStatus.CREATED,
        db_index=True,
    )

    priority = models.CharField(
        max_length=20,
        choices=AIJobPriority.choices,
        default=AIJobPriority.NORMAL,
        db_index=True,
    )

    input_storage_key = models.CharField(
        max_length=1024,
        blank=True,
    )

    input_checksum_sha256 = models.CharField(
        max_length=64,
        blank=True,
    )

    output_storage_key = models.CharField(
        max_length=1024,
        blank=True,
    )

    celery_task_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    queued_at = models.DateTimeField(
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

    processing_time_ms = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )

    error_code = models.CharField(
        max_length=100,
        blank=True,
    )

    error_message = models.TextField(
        blank=True,
    )

    worker_id = models.CharField(
        max_length=255,
        blank=True,
    )

    class Meta:
        db_table = "ai_inference_jobs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "status",
                    "priority",
                ],
                name="ai_job_status_priority_idx",
            ),
            models.Index(
                fields=[
                    "model_version",
                    "created_at",
                ],
                name="ai_job_model_created_idx",
            ),
            models.Index(
                fields=[
                    "imaging_study",
                    "status",
                ],
                name="ai_job_study_status_idx",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.job_reference:
            self.job_reference = (
                f"AI-{uuid.uuid4().hex[:16].upper()}"
            )

        super().save(*args, **kwargs)

    def clean(self):
        if self.imaging_study:
            if (
                self.model_version.model.status
                != AIModelStatus.PRODUCTION
                and self.model_version.is_active is False
            ):
                raise ValidationError(
                    "The selected AI model version is not active "
                    "for inference."
                )

    def __str__(self):
        return self.job_reference


class PredictionType(models.TextChoices):
    CLASSIFICATION = "CLASSIFICATION", "Classification"
    DETECTION = "DETECTION", "Detection"
    SEGMENTATION = "SEGMENTATION", "Segmentation"
    RISK = "RISK", "Risk Score"
    OTHER = "OTHER", "Other"


class Prediction(BaseModel):
    """
    Machine-generated prediction produced by an AI inference job.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    job = models.ForeignKey(
        AIInferenceJob,
        on_delete=models.PROTECT,
        related_name="predictions",
    )

    prediction_type = models.CharField(
        max_length=30,
        choices=PredictionType.choices,
    )

    label = models.CharField(
        max_length=255,
        db_index=True,
    )

    probability = models.DecimalField(
        max_digits=7,
        decimal_places=6,
    )

    severity = models.CharField(
        max_length=50,
        blank=True,
    )

    anatomical_location = models.CharField(
        max_length=255,
        blank=True,
    )

    coordinates = models.JSONField(
        default=dict,
        blank=True,
    )

    mask_storage_key = models.CharField(
        max_length=1024,
        blank=True,
    )

    explanation = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "ai_predictions"
        ordering = ["-probability"]
        indexes = [
            models.Index(
                fields=[
                    "job",
                    "label",
                ],
                name="prediction_job_label_idx",
            ),
            models.Index(
                fields=[
                    "label",
                    "probability",
                ],
                name="prediction_label_prob_idx",
            ),
        ]

    def clean(self):
        if not 0 <= self.probability <= 1:
            raise ValidationError(
                "Prediction probability must be between 0 and 1."
            )

    def __str__(self):
        return (
            f"{self.label} "
            f"({self.probability})"
        )


class HumanReviewStatus(models.TextChoices):
    NOT_REQUIRED = "NOT_REQUIRED", "Not Required"
    PENDING = "PENDING", "Pending"
    IN_REVIEW = "IN_REVIEW", "In Review"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    MODIFIED = "MODIFIED", "Modified"


class AIHumanReview(BaseModel):
    """
    Clinical review of AI-generated results.

    AI output is never treated as a final clinical decision merely
    because the inference completed successfully.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    job = models.OneToOneField(
        AIInferenceJob,
        on_delete=models.PROTECT,
        related_name="human_review",
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ai_reviews",
    )

    status = models.CharField(
        max_length=20,
        choices=HumanReviewStatus.choices,
        default=HumanReviewStatus.PENDING,
        db_index=True,
    )

    reviewer_comments = models.TextField(
        blank=True,
    )

    corrected_findings = models.JSONField(
        default=dict,
        blank=True,
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "ai_human_reviews"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "status",
                    "created_at",
                ],
                name="ai_review_status_idx",
            ),
        ]

    def clean(self):
        if (
            self.status
            in {
                HumanReviewStatus.APPROVED,
                HumanReviewStatus.REJECTED,
                HumanReviewStatus.MODIFIED,
            }
            and not self.reviewer
        ):
            raise ValidationError(
                "A completed review must have a reviewer."
            )

    def __str__(self):
        return self.job.job_reference