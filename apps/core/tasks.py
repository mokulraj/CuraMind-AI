from celery import shared_task


@shared_task(
    bind=True,
    name="apps.core.tasks.health_check",
)
def health_check(self):
    return {
        "status": "ok",
        "service": "CuraMind AI",
        "task_id": self.request.id,
    }