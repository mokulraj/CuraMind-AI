from django.urls import include, path

from .views import HealthCheckView


app_name = "api"


urlpatterns = [
    path(
        "health/",
        HealthCheckView.as_view(),
        name="health",
    ),

    path(
        "auth/",
        include(
            "apps.users.authentication.urls"
        ),
    ),

    path(
        "core/",
        include(
            "apps.core.urls"
        ),
    ),

    path(
        "appointments/",
        include(
            "apps.appointments.urls"
        ),
    ),

    path(
        "emr/",
        include(
            "apps.emr.urls"
        ),
    ),

    path(
        "imaging/",
        include(
            "apps.imaging.urls"
        ),
    ),

    path(
        "ai/",
        include(
            "apps.ai_pipeline.urls"
        ),
    ),

    path(
        "audit/",
        include(
            "apps.audit.urls"
        ),
    ),

    path(
        "notifications/",
        include(
            "apps.notifications.urls"
        ),
    ),

    path(
        "dashboard/",
        include(
            "apps.dashboard.urls"
        ),
    ),

    path(
        "payments/",
        include(
            "apps.payments.urls"
        ),
    ),

    path(
        "reports/",
        include(
            "apps.reports.urls"
        ),
    ),
]