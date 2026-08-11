from .base import *


DEBUG = False

ENVIRONMENT = "testing"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get(
            "TEST_POSTGRES_DB",
            "curamind_ai_test",
        ),
        "USER": os.environ.get(
            "TEST_POSTGRES_USER",
            "curamind_app",
        ),
        "PASSWORD": os.environ.get(
            "TEST_POSTGRES_PASSWORD",
            os.environ.get(
                "POSTGRES_PASSWORD",
                "",
            ),
        ),
        "HOST": os.environ.get(
            "TEST_POSTGRES_HOST",
            os.environ.get(
                "POSTGRES_HOST",
                "127.0.0.1",
            ),
        ),
        "PORT": os.environ.get(
            "TEST_POSTGRES_PORT",
            os.environ.get(
                "POSTGRES_PORT",
                "5432",
            ),
        ),
        "CONN_MAX_AGE": 0,
        "OPTIONS": {
            "connect_timeout": 10,
        },
    },
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"