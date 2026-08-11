from celery import shared_task


@shared_task(
    bind=True,
    name="apps.ai_pipeline.tasks.process_ai_job",
)
def process_ai_job(
    self,
    inference_job_id,
):
    return {
        "status": "queued",
        "inference_job_id": inference_job_id,
        "task_id": self.request.id,
    }