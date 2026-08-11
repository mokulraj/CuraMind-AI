from .base import *


# ============================================================
# DEVELOPMENT
# ============================================================

DEBUG = True

ENVIRONMENT = "development"


# ============================================================
# EMAIL
# ============================================================

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
)

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
)

EMAIL_USE_TLS = False

EMAIL_USE_SSL = False

EMAIL_TIMEOUT = 10

# ============================================================
# CORS
# ============================================================

CORS_ALLOW_ALL_ORIGINS = True