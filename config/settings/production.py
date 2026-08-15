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

SECURE_SSL_REDIRECT = False

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
# 
#============================================================

# ============================================================
# STORAGE
# ============================================================

AWS_STORAGE_BUCKET_NAME = os.environ.get(
    "AWS_STORAGE_BUCKET_NAME",
    "",
).strip()

AWS_S3_ENDPOINT_URL = (
    os.environ.get(
        "AWS_S3_ENDPOINT_URL",
        "",
    ).strip()
    or None
)

AWS_S3_REGION_NAME = os.environ.get(
    "AWS_S3_REGION_NAME",
    "ap-south-1",
).strip()

AWS_S3_SIGNATURE_VERSION = os.environ.get(
    "AWS_S3_SIGNATURE_VERSION",
    "s3v4",
).strip()

AWS_S3_ADDRESSING_STYLE = os.environ.get(
    "AWS_S3_ADDRESSING_STYLE",
    "virtual",
).strip()

AWS_QUERYSTRING_EXPIRE = int(
    os.environ.get(
        "AWS_QUERYSTRING_EXPIRE",
        "300",
    )
)

AWS_S3_CACHE_CONTROL = os.environ.get(
    "AWS_S3_CACHE_CONTROL",
    "max-age=86400",
)

AWS_S3_VERIFY = (
    os.environ.get(
        "AWS_S3_VERIFY",
        "True",
    ).lower()
    == "true"
)

AWS_S3_USE_SSL = (
    os.environ.get(
        "AWS_S3_USE_SSL",
        "True",
    ).lower()
    == "true"
)


# ------------------------------------------------------------
# Use S3 only when a bucket is actually configured.
# Otherwise use Docker's local volumes.
# ------------------------------------------------------------

if AWS_STORAGE_BUCKET_NAME:

    STORAGES = {
        "default": {
            "BACKEND": (
                "storage.backends.CuraMindMediaStorage"
            ),
        },
        "staticfiles": {
            "BACKEND": (
                "storage.backends.CuraMindStaticStorage"
            ),
        },
    }

else:

    STORAGES = {
        "default": {
            "BACKEND": (
                "django.core.files.storage."
                "FileSystemStorage"
            ),
        },
        "staticfiles": {
            "BACKEND": (
                "django.contrib.staticfiles.storage."
                "StaticFilesStorage"
            ),
        },
    }
# CORS
# ============================================================

CORS_ALLOW_ALL_ORIGINS = False


# ============================================================
# EMAIL
# ============================================================
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend",
)

# ============================================================
# AUTHENTICATION REDIRECTS
# ============================================================

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/login/"