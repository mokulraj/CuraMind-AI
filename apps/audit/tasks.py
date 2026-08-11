from celery import shared_task

from apps.audit.models import AuditEvent


@shared_task(
    bind=True,
    name="apps.audit.tasks.audit_health_check",
)
def audit_health_check(
    self,
):
    count = AuditEvent.objects.count()

    return {
        "status": "ok",
        "audit_event_count": count,
        "task_id": self.request.id,
    }