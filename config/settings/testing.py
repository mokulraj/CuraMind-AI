from .base import *


# ============================================================
# TESTING
# ============================================================

DEBUG = False

ENVIRONMENT = "testing"


# ============================================================
# TEST DATABASE
# ============================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",

        "NAME": env(
            "TEST_POSTGRES_DB",
            default="curamind_ai_test",
        ),

        "USER": env(
            "TEST_POSTGRES_USER",
            default="curamind_app",
        ),

        "PASSWORD": env(
            "TEST_POSTGRES_PASSWORD",
            default=env(
                "POSTGRES_PASSWORD",
                default="",
            ),
        ),

        "HOST": env(
            "TEST_POSTGRES_HOST",
            default=env(
                "POSTGRES_HOST",
                default="127.0.0.1",
            ),
        ),

        "PORT": env(
            "TEST_POSTGRES_PORT",
            default=env(
                "POSTGRES_PORT",
                default="5432",
            ),
        ),

        "CONN_MAX_AGE": 0,

        "OPTIONS": {
            "connect_timeout": 10,
        },
    },
}


# ============================================================
# PASSWORD HASHING
# ============================================================

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]


# ============================================================
# EMAIL
# ============================================================

EMAIL_BACKEND = (
    "django.core.mail.backends.locmem.EmailBackend"
)


# ============================================================
# TEST REDIS
# ============================================================

TEST_REDIS_HOST = env(
    "TEST_REDIS_HOST",
    default=env(
        "REDIS_HOST",
        default="127.0.0.1",
    ),
)

TEST_REDIS_PORT = env(
    "TEST_REDIS_PORT",
    default=env(
        "REDIS_PORT",
        default="6379",
    ),
)

TEST_REDIS_DB = env(
    "TEST_REDIS_DB",
    default="15",
)

TEST_REDIS_PASSWORD = env(
    "TEST_REDIS_PASSWORD",
    default=env(
        "REDIS_PASSWORD",
        default="",
    ),
)


# ============================================================
# TEST REDIS URL
# ============================================================

if TEST_REDIS_PASSWORD:
    TEST_REDIS_URL = (
        f"redis://:{TEST_REDIS_PASSWORD}"
        f"@{TEST_REDIS_HOST}:"
        f"{TEST_REDIS_PORT}/"
        f"{TEST_REDIS_DB}"
    )
else:
    TEST_REDIS_URL = (
        f"redis://"
        f"{TEST_REDIS_HOST}:"
        f"{TEST_REDIS_PORT}/"
        f"{TEST_REDIS_DB}"
    )


# ============================================================
# TEST CACHE
# ============================================================

CACHES = {
    "default": {
        "BACKEND": (
            "django_redis.cache.RedisCache"
        ),

        "LOCATION": TEST_REDIS_URL,

        "OPTIONS": {
            "CLIENT_CLASS": (
                "django_redis.client.DefaultClient"
            ),

            "SOCKET_CONNECT_TIMEOUT": 5,

            "SOCKET_TIMEOUT": 5,

            "IGNORE_EXCEPTIONS": False,
        },

        "KEY_PREFIX": "curamind-test",

        "TIMEOUT": 60,
    },
}


# ============================================================
# TEST SESSIONS
# ============================================================

SESSION_ENGINE = (
    "django.contrib.sessions.backends.cache"
)

SESSION_CACHE_ALIAS = "default"


# ============================================================
# TEST CELERY REDIS
# ============================================================

TEST_CELERY_BROKER_DB = env(
    "TEST_CELERY_BROKER_DB",
    default="11",
)

TEST_CELERY_RESULT_DB = env(
    "TEST_CELERY_RESULT_DB",
    default="12",
)


# ============================================================
# TEST CELERY BROKER
# ============================================================

if TEST_REDIS_PASSWORD:

    CELERY_BROKER_URL = (
        f"redis://:{TEST_REDIS_PASSWORD}"
        f"@{TEST_REDIS_HOST}:"
        f"{TEST_REDIS_PORT}/"
        f"{TEST_CELERY_BROKER_DB}"
    )

    CELERY_RESULT_BACKEND = (
        f"redis://:{TEST_REDIS_PASSWORD}"
        f"@{TEST_REDIS_HOST}:"
        f"{TEST_REDIS_PORT}/"
        f"{TEST_CELERY_RESULT_DB}"
    )

else:

    CELERY_BROKER_URL = (
        f"redis://"
        f"{TEST_REDIS_HOST}:"
        f"{TEST_REDIS_PORT}/"
        f"{TEST_CELERY_BROKER_DB}"
    )

    CELERY_RESULT_BACKEND = (
        f"redis://"
        f"{TEST_REDIS_HOST}:"
        f"{TEST_REDIS_PORT}/"
        f"{TEST_CELERY_RESULT_DB}"
    )


# ============================================================
# TEST CELERY EXECUTION
# ============================================================

CELERY_TASK_ALWAYS_EAGER = True

CELERY_TASK_EAGER_PROPAGATES = True

CELERY_TASK_RESULT_EXPIRES = 60