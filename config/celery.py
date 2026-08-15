import os
from celery import Celery


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings.development",
)


app = Celery(
    "curamind_ai",
)


app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)


app.conf.update(
    broker_url="redis://127.0.0.1:6379/0",
    result_backend="redis://127.0.0.1:6379/0",

    task_default_queue="default",

    task_default_exchange="default",
    task_default_exchange_type="direct",
    task_default_routing_key="default",

    task_ignore_result=False,

    result_expires=3600,

    broker_connection_retry_on_startup=True,

    task_track_started=True,
)


app.conf.task_routes = {
    "apps.core.email.tasks.send_email_task": {
        "queue": "default",
        "routing_key": "default",
    },
    "apps.core.email.tasks.email_health_check": {
        "queue": "default",
        "routing_key": "default",
    },
}


app.conf.imports = (
    "apps.core.email.tasks",
    "apps.core.tasks",
    "apps.audit.tasks",
    "apps.ai_pipeline.tasks",
    "apps.imaging.tasks",
    "apps.notifications.tasks",
)


@app.task(
    bind=True,
    ignore_result=False,
)
def debug_task(self):
    return {
        "status": "ok",
        "task": "debug_task",
        "request_id": self.request.id,
    }