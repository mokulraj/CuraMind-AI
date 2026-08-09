import uuid

from django.db import transaction

from apps.ai_pipeline.models import (
    AIInferenceJob,
    AIModelVersion,
)


class InferenceService:
    """
    Creates and manages AI inference jobs.

    Actual model execution is intentionally separated from
    database job creation. Celery integration is implemented
    later in the project.
    """

    @staticmethod
    @transaction.atomic
    def create_inference_job(
        *,
        model_version,
        imaging_study,
        requested_by,
        priority=None,
        input_data=None,
    ):
        if not isinstance(
            model_version,
            AIModelVersion,
        ):
            raise ValueError(
                "model_version must be an AIModelVersion."
            )

        job = AIInferenceJob.objects.create(
            job_reference=(
                f"AI-{uuid.uuid4().hex[:12].upper()}"
            ),
            model_version=model_version,
            imaging_study=imaging_study,
            requested_by=requested_by,
            priority=priority,
            input_data=input_data or {},
        )

        return job

    @staticmethod
    @transaction.atomic
    def mark_job_failed(
        *,
        job,
        failure_reason,
    ):
        job.status = "FAILED"

        if hasattr(job, "failure_reason"):
            job.failure_reason = failure_reason

        update_fields = [
            "status",
            "updated_at",
        ]

        if hasattr(job, "failure_reason"):
            update_fields.append("failure_reason")

        job.save(
            update_fields=update_fields
        )

        return job