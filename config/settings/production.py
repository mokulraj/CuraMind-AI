from .base import *


# ============================================================
# PRODUCTION
# ============================================================

DEBUG = False

ENVIRONMENT = "production"


# ============================================================
# ALLOWED HOSTS
# ============================================================

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS"
)


# ============================================================
# SECURITY
# ============================================================

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True


EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend",
)

EMAIL_HOST = os.environ.get(
    "EMAIL_HOST"
)

EMAIL_PORT = int(
    os.environ.get(
        "EMAIL_PORT",
        "587",
    )
)

EMAIL_HOST_USER = os.environ.get(
    "EMAIL_HOST_USER"
)

EMAIL_HOST_PASSWORD = os.environ.get(
    "EMAIL_HOST_PASSWORD"
)

EMAIL_USE_TLS = (
    os.environ.get(
        "EMAIL_USE_TLS",
        "True",
    ).lower()
    == "true"
)

EMAIL_USE_SSL = (
    os.environ.get(
        "EMAIL_USE_SSL",
        "False",
    ).lower()
    == "true"
)

EMAIL_TIMEOUT = int(
    os.environ.get(
        "EMAIL_TIMEOUT",
        "10",
    )
)

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL"
)

SERVER_EMAIL = os.environ.get(
    "SERVER_EMAIL",
    DEFAULT_FROM_EMAIL,
)

EMAIL_REPLY_TO = os.environ.get(
    "EMAIL_REPLY_TO",
    "",
)
# ============================================================
# CORS
# ============================================================

CORS_ALLOW_ALL_ORIGINS = False


# ============================================================
# EMAIL
# ============================================================

EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"
)