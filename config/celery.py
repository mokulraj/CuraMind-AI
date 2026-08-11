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


app.autodiscover_tasks()


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