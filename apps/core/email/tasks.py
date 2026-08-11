from celery import shared_task

from apps.core.email.services import (
    send_email,
)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_kwargs={
        "max_retries": 3,
    },
    name="apps.core.email.tasks.send_email_task",
)
def send_email_task(
    self,
    *,
    recipient,
    subject,
    text_content,
    html_content=None,
    reply_to=None,
):
    sent_count = send_email(
        recipient=recipient,
        subject=subject,
        text_content=text_content,
        html_content=html_content,
        reply_to=reply_to,
    )

    return {
        "status": "sent",
        "recipient": recipient,
        "sent_count": sent_count,
        "task_id": self.request.id,
    }


@shared_task(
    bind=True,
    name="apps.core.email.tasks.email_health_check",
)
def email_health_check(
    self,
):
    from django.conf import settings

    return {
        "status": "configured",
        "backend": settings.EMAIL_BACKEND,
        "host": settings.EMAIL_HOST,
        "port": settings.EMAIL_PORT,
        "use_tls": settings.EMAIL_USE_TLS,
        "use_ssl": settings.EMAIL_USE_SSL,
        "task_id": self.request.id,
    }