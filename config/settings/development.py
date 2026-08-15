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



DEFAULT_FILE_STORAGE = (
    "django.core.files.storage.FileSystemStorage"
)

STATICFILES_STORAGE = (
    "django.contrib.staticfiles.storage.StaticFilesStorage"
)

MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "/media/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = "/static/"

# ============================================================
# CORS
# ============================================================

CORS_ALLOW_ALL_ORIGINS = True