from celery import shared_task
from django.conf import settings

from apps.ai_pipeline.services.inference import (
    AIInferenceService,
)


@shared_task(
    bind=True,
    name="apps.ai_pipeline.tasks.process_ai_job",
)
def process_ai_job(
    self,
    features,
):
    service = AIInferenceService(
        model_path=settings.AI_MODEL_PATH,
        model_version=settings.AI_MODEL_VERSION,
    )

    result = service.predict(
        features
    )

    return {
        "status": "completed",
        "prediction": result.prediction,
        "probabilities": result.probabilities,
        "model_version": result.model_version,
        "task_id": self.request.id,
    }


@shared_task(
    bind=True,
    name="apps.ai_pipeline.tasks.ai_model_health_check",
)
def ai_model_health_check(
    self,
):
    service = AIInferenceService(
        model_path=settings.AI_MODEL_PATH,
        model_version=settings.AI_MODEL_VERSION,
    )

    result = service.health_check()

    result["task_id"] = self.request.id

    return result