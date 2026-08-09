from django.contrib import admin

from .models import (
    AIHumanReview,
    AIInferenceJob,
    AIModel,
    AIModelVersion,
    Prediction,
)


@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "display_name",
        "model_type",
        "framework",
        "status",
        "is_clinical_use_approved",
    )
    list_filter = (
        "model_type",
        "framework",
        "status",
        "is_clinical_use_approved",
    )
    search_fields = (
        "name",
        "display_name",
        "description",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(AIModelVersion)
class AIModelVersionAdmin(admin.ModelAdmin):
    list_display = (
        "model",
        "version",
        "is_active",
        "accuracy",
        "sensitivity",
        "specificity",
        "auc",
    )
    list_filter = (
        "is_active",
    )
    search_fields = (
        "model__name",
        "version",
        "artifact_sha256",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(AIInferenceJob)
class AIInferenceJobAdmin(admin.ModelAdmin):
    list_display = (
        "job_reference",
        "model_version",
        "imaging_study",
        "status",
        "priority",
        "created_at",
        "completed_at",
    )
    list_filter = (
        "status",
        "priority",
    )
    search_fields = (
        "job_reference",
        "model_version__model__name",
        "imaging_study__accession_number",
        "celery_task_id",
    )
    date_hierarchy = "created_at"
    readonly_fields = (
        "id",
        "job_reference",
        "created_at",
        "updated_at",
    )


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = (
        "job",
        "prediction_type",
        "label",
        "probability",
        "severity",
    )
    list_filter = (
        "prediction_type",
        "severity",
    )
    search_fields = (
        "label",
        "anatomical_location",
        "job__job_reference",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(AIHumanReview)
class AIHumanReviewAdmin(admin.ModelAdmin):
    list_display = (
        "job",
        "reviewer",
        "status",
        "reviewed_at",
    )
    list_filter = (
        "status",
    )
    search_fields = (
        "job__job_reference",
        "reviewer__email",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )