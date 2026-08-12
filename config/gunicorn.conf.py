import multiprocessing
import os


# ---------------------------------------------------------
# Server
# ---------------------------------------------------------

bind = os.getenv(
    "GUNICORN_BIND",
    "0.0.0.0:8000",
)


# ---------------------------------------------------------
# Worker configuration
# ---------------------------------------------------------

_default_workers = max(
    multiprocessing.cpu_count() * 2 + 1,
    2,
)

workers = int(
    os.getenv(
        "GUNICORN_WORKERS",
        str(_default_workers),
    )
)

worker_class = os.getenv(
    "GUNICORN_WORKER_CLASS",
    "gthread",
)

threads = int(
    os.getenv(
        "GUNICORN_THREADS",
        "2",
    )
)


# ---------------------------------------------------------
# Timeouts
# ---------------------------------------------------------

timeout = int(
    os.getenv(
        "GUNICORN_TIMEOUT",
        "120",
    )
)

graceful_timeout = int(
    os.getenv(
        "GUNICORN_GRACEFUL_TIMEOUT",
        "30",
    )
)

keepalive = int(
    os.getenv(
        "GUNICORN_KEEPALIVE",
        "5",
    )
)


# ---------------------------------------------------------
# Request recycling
# ---------------------------------------------------------

max_requests = int(
    os.getenv(
        "GUNICORN_MAX_REQUESTS",
        "1000",
    )
)

max_requests_jitter = int(
    os.getenv(
        "GUNICORN_MAX_REQUESTS_JITTER",
        "100",
    )
)


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

accesslog = "-"

errorlog = "-"

loglevel = os.getenv(
    "GUNICORN_LOG_LEVEL",
    "info",
)


# ---------------------------------------------------------
# Process naming
# ---------------------------------------------------------

proc_name = os.getenv(
    "GUNICORN_PROC_NAME",
    "curamind-gunicorn",
)


# ---------------------------------------------------------
# Worker lifecycle
# ---------------------------------------------------------

preload_app = False

daemon = False

forwarded_allow_ips = os.getenv(
    "GUNICORN_FORWARDED_ALLOW_IPS",
    "*",
)


# ---------------------------------------------------------
# Security / request limits
# ---------------------------------------------------------

limit_request_line = int(
    os.getenv(
        "GUNICORN_LIMIT_REQUEST_LINE",
        "4094",
    )
)

limit_request_fields = int(
    os.getenv(
        "GUNICORN_LIMIT_REQUEST_FIELDS",
        "100",
    )
)

limit_request_field_size = int(
    os.getenv(
        "GUNICORN_LIMIT_REQUEST_FIELD_SIZE",
        "8190",
    )
)


# ---------------------------------------------------------
# Server hooks
# ---------------------------------------------------------

def on_starting(server):
    server.log.info(
        "CuraMind AI Gunicorn starting."
    )


def when_ready(server):
    server.log.info(
        "CuraMind AI Gunicorn is ready."
    )


def worker_int(worker):
    worker.log.info(
        "Gunicorn worker received INT/QUIT signal."
    )


def worker_abort(worker):
    worker.log.warning(
        "Gunicorn worker aborted."
    )


def on_exit(server):
    server.log.info(
        "CuraMind AI Gunicorn shutting down."
    )