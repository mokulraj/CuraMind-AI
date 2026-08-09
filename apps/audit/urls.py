from rest_framework.routers import DefaultRouter

from .views import (
    AuditEventViewSet,
    AuthenticationEventViewSet,
    PatientDataAccessLogViewSet,
    SecurityEventViewSet,
)


app_name = "audit"


router = DefaultRouter()

router.register(
    "events",
    AuditEventViewSet,
    basename="event",
)

router.register(
    "authentication-events",
    AuthenticationEventViewSet,
    basename="authentication-event",
)

router.register(
    "patient-access-logs",
    PatientDataAccessLogViewSet,
    basename="patient-access-log",
)

router.register(
    "security-events",
    SecurityEventViewSet,
    basename="security-event",
)


urlpatterns = router.urls