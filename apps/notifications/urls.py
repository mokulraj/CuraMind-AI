from rest_framework.routers import DefaultRouter

from .views import (
    NotificationDeliveryAttemptViewSet,
    NotificationPreferenceViewSet,
    NotificationTemplateViewSet,
    NotificationViewSet,
)


app_name = "notifications"


router = DefaultRouter()

router.register(
    "notifications",
    NotificationViewSet,
    basename="notification",
)

router.register(
    "templates",
    NotificationTemplateViewSet,
    basename="template",
)

router.register(
    "delivery-attempts",
    NotificationDeliveryAttemptViewSet,
    basename="delivery-attempt",
)

router.register(
    "preferences",
    NotificationPreferenceViewSet,
    basename="preference",
)


urlpatterns = router.urls