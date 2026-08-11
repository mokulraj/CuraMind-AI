from celery import shared_task


@shared_task(
    bind=True,
    name="apps.notifications.tasks.send_notification",
)
def send_notification(
    self,
    notification_id,
):
    return {
        "status": "queued",
        "notification_id": notification_id,
        "task_id": self.request.id,
    }