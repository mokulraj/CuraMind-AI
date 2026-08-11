from pathlib import Path
from datetime import timedelta
import os

import environ


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

env = environ.Env()

environ.Env.read_env(BASE_DIR / ".env")


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool(
    "DEBUG",
    default=False,
)

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=[],
)


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = env(
    "LANGUAGE_CODE",
    default="en-us",
)

TIME_ZONE = env(
    "TIME_ZONE",
    default="Asia/Kolkata",
)

USE_I18N = True

USE_TZ = True


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    # --------------------------------------------------------
    # Django
    # --------------------------------------------------------

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # --------------------------------------------------------
    # Third-party
    # --------------------------------------------------------

    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "drf_spectacular",

    # --------------------------------------------------------
    # CuraMind AI applications
    # --------------------------------------------------------

    "apps.users.apps.UsersConfig",
    "apps.core",
    "apps.appointments",
    "apps.emr",
    "apps.imaging",
    "apps.ai_pipeline",
    "apps.audit",
    "apps.notifications",
    "apps.dashboard",
    "apps.payments",
    "apps.reports",
    "apps.api",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URL CONFIGURATION
# ============================================================

ROOT_URLCONF = "config.urls"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": (
            "django.template.backends.django.DjangoTemplates"
        ),

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ============================================================
# WSGI / ASGI
# ============================================================

WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"


# ============================================================
# DATABASE - POSTGRESQL
# ============================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",

        "NAME": env(
            "POSTGRES_DB",
            default="curamind_ai",
        ),

        "USER": env(
            "POSTGRES_USER",
            default="curamind_app",
        ),

        "PASSWORD": env(
            "POSTGRES_PASSWORD",
            default="",
        ),

        "HOST": env(
            "POSTGRES_HOST",
            default="127.0.0.1",
        ),

        "PORT": env(
            "POSTGRES_PORT",
            default="5432",
        ),

        "CONN_MAX_AGE": 60,

        "CONN_HEALTH_CHECKS": True,

        "OPTIONS": {
            "connect_timeout": 10,
        },
    },
}


# ============================================================
# REDIS
# ============================================================

REDIS_URL = env(
    "REDIS_URL",
    default="redis://127.0.0.1:6379/1",
)


# ============================================================
# DJANGO CACHE
# ============================================================

CACHES = {
    "default": {
        "BACKEND": (
            "django_redis.cache.RedisCache"
        ),

        "LOCATION": REDIS_URL,

        "OPTIONS": {
            "CLIENT_CLASS": (
                "django_redis.client.DefaultClient"
            ),

            "SOCKET_CONNECT_TIMEOUT": 5,

            "SOCKET_TIMEOUT": 5,

            "IGNORE_EXCEPTIONS": False,
        },

        "KEY_PREFIX": "curamind",

        "TIMEOUT": 300,
    },
}


# ============================================================
# DJANGO SESSIONS
# ============================================================

SESSION_ENGINE = (
    "django.contrib.sessions.backends.cache"
)

SESSION_CACHE_ALIAS = "default"

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SAMESITE = "Lax"

SESSION_COOKIE_AGE = 60 * 60 * 8

SESSION_SAVE_EVERY_REQUEST = False


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ============================================================
# CUSTOM USER MODEL
# ============================================================

AUTH_USER_MODEL = "users.User"


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / os.environ.get(
    "MEDIA_ROOT",
    "media",
)


# ============================================================
# FILE UPLOAD LIMITS
# ============================================================

MAX_UPLOAD_SIZE = int(
    os.environ.get(
        "MAX_UPLOAD_SIZE",
        str(10 * 1024 * 1024),
    )
)

MAX_IMAGE_UPLOAD_SIZE = int(
    os.environ.get(
        "MAX_IMAGE_UPLOAD_SIZE",
        str(10 * 1024 * 1024),
    )
)

MAX_REPORT_UPLOAD_SIZE = int(
    os.environ.get(
        "MAX_REPORT_UPLOAD_SIZE",
        str(25 * 1024 * 1024),
    )
)

FILE_UPLOAD_MAX_MEMORY_SIZE = int(
    os.environ.get(
        "FILE_UPLOAD_MAX_MEMORY_SIZE",
        str(10 * 1024 * 1024),
    )
)

DATA_UPLOAD_MAX_MEMORY_SIZE = int(
    os.environ.get(
        "DATA_UPLOAD_MAX_MEMORY_SIZE",
        str(10 * 1024 * 1024),
    )
)


# ============================================================
# ALLOWED FILE EXTENSIONS
# ============================================================

ALLOWED_DOCUMENT_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".txt",
}

ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

ALLOWED_REPORT_EXTENSIONS = {
    ".pdf",
}


# ============================================================
# DJANGO REST FRAMEWORK
# ============================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),

    "DEFAULT_SCHEMA_CLASS": (
        "drf_spectacular.openapi.AutoSchema"
    ),

    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
}


# ============================================================
# SIMPLE JWT
# ============================================================

SIMPLE_JWT = {
    # --------------------------------------------------------
    # Access token
    # --------------------------------------------------------

    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=30
    ),

    # --------------------------------------------------------
    # Refresh token
    # --------------------------------------------------------

    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=7
    ),

    # --------------------------------------------------------
    # Rotate refresh tokens
    # --------------------------------------------------------

    "ROTATE_REFRESH_TOKENS": True,

    # --------------------------------------------------------
    # Blacklist old refresh token
    # --------------------------------------------------------

    "BLACKLIST_AFTER_ROTATION": True,

    # --------------------------------------------------------
    # Authorization header
    # --------------------------------------------------------

    "AUTH_HEADER_TYPES": (
        "Bearer",
    ),
}


# ============================================================
# DRF SPECTACULAR / OPENAPI
# ============================================================

SPECTACULAR_SETTINGS = {
    "TITLE": "CuraMind AI API",

    "DESCRIPTION": "Healthcare SaaS API",

    "VERSION": "1.0.0",
}


# ============================================================
# CORS
# ============================================================

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


# ============================================================
# CELERY
# ============================================================

CELERY_BROKER_URL = env(
    "CELERY_BROKER_URL",
    default="redis://127.0.0.1:6379/0",
)

CELERY_RESULT_BACKEND = env(
    "CELERY_RESULT_BACKEND",
    default="redis://127.0.0.1:6379/0",
)


# ============================================================
# CELERY SERIALIZATION
# ============================================================

CELERY_ACCEPT_CONTENT = [
    "json",
]

CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_SERIALIZER = "json"

CELERY_EVENT_SERIALIZER = "json"


# ============================================================
# CELERY TIMEZONE
# ============================================================

CELERY_TIMEZONE = TIME_ZONE

CELERY_ENABLE_UTC = True


# ============================================================
# CELERY TASK TRACKING
# ============================================================

CELERY_TASK_TRACK_STARTED = True

CELERY_TASK_SEND_SENT_EVENT = True

CELERY_WORKER_SEND_TASK_EVENTS = True


# ============================================================
# CELERY EAGER EXECUTION
# ============================================================

CELERY_TASK_ALWAYS_EAGER = (
    os.environ.get(
        "CELERY_TASK_ALWAYS_EAGER",
        "False",
    ).lower()
    == "true"
)

CELERY_TASK_EAGER_PROPAGATES = (
    os.environ.get(
        "CELERY_TASK_EAGER_PROPAGATES",
        "False",
    ).lower()
    == "true"
)


# ============================================================
# CELERY RESULT EXPIRATION
# ============================================================

CELERY_TASK_RESULT_EXPIRES = int(
    os.environ.get(
        "CELERY_TASK_RESULT_EXPIRES",
        "3600",
    )
)


# ============================================================
# CELERY WORKER
# ============================================================

CELERY_WORKER_CONCURRENCY = int(
    os.environ.get(
        "CELERY_WORKER_CONCURRENCY",
        "2",
    )
)


# ============================================================
# CELERY BROKER CONNECTION
# ============================================================

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_BROKER_CONNECTION_MAX_RETRIES = 10


# ============================================================
# CELERY TRANSPORT
# ============================================================

CELERY_BROKER_TRANSPORT_OPTIONS = {
    "visibility_timeout": 3600,
}

CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = {
    "visibility_timeout": 3600,
    "global_keyprefix": "curamind_celery_",
}


# ============================================================
# CELERY TASK ROUTING
# ============================================================

CELERY_TASK_ROUTES = {
    "apps.ai_pipeline.tasks.*": {
        "queue": "ai",
    },

    "apps.notifications.tasks.*": {
        "queue": "notifications",
    },

    "apps.core.tasks.*": {
        "queue": "default",
    },
}


# ============================================================
# CELERY QUEUES
# ============================================================

from kombu import Queue

CELERY_TASK_QUEUES = (
    Queue("default"),
    Queue("ai"),
    Queue("notifications"),
)


# ============================================================
# LOGGING
# ============================================================

LOGGING = {
    "version": 1,

    "disable_existing_loggers": False,

    "handlers": {
        "file": {
            "level": "INFO",

            "class": "logging.FileHandler",

            "filename": BASE_DIR / "logs" / "django.log",
        },
    },

    "loggers": {
        "django": {
            "handlers": [
                "file",
            ],

            "level": "INFO",

            "propagate": True,
        },
    },
}


# ============================================================
# DEFAULT AUTO FIELD
# ============================================================

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)