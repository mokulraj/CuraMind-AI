from rest_framework.routers import DefaultRouter

from .views import (
    AddressViewSet,
    DepartmentViewSet,
    EmergencyContactViewSet,
    OrganizationViewSet,
)


app_name = "core"


router = DefaultRouter()

router.register(
    "organizations",
    OrganizationViewSet,
    basename="organization",
)

router.register(
    "departments",
    DepartmentViewSet,
    basename="department",
)

router.register(
    "addresses",
    AddressViewSet,
    basename="address",
)

router.register(
    "emergency-contacts",
    EmergencyContactViewSet,
    basename="emergency-contact",
)


urlpatterns = router.urls