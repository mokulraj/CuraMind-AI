from apps.ai_pipeline.models import (
    AIInferenceJob,
    AIModel,
    AIModelVersion,
    Prediction,
)


class InferenceRepository:
    """
    Database access for AI models and inference jobs.
    """

    @staticmethod
    def get_model_by_id(
        model_id,
    ):
        return (
            AIModel.objects
            .filter(pk=model_id)
            .first()
        )

    @staticmethod
    def get_active_versions(
        model_id,
    ):
        return (
            AIModelVersion.objects
            .filter(
                model_id=model_id,
                is_active=True,
            )
            .order_by("-version")
        )

    @staticmethod
    def get_job_by_id(
        job_id,
    ):
        return (
            AIInferenceJob.objects
            .select_related(
                "model_version",
                "imaging_study",
                "requested_by",
            )
            .filter(pk=job_id)
            .first()
        )

    @staticmethod
    def get_job_by_reference(
        job_reference,
    ):
        return (
            AIInferenceJob.objects
            .select_related(
                "model_version",
                "imaging_study",
                "requested_by",
            )
            .filter(
                job_reference=job_reference
            )
            .first()
        )

    @staticmethod
    def list_predictions(
        job_id,
    ):
        return (
            Prediction.objects
            .filter(
                job_id=job_id
            )
            .order_by("-probability")
        )