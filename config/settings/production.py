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