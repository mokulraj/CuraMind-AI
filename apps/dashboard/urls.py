from rest_framework.routers import DefaultRouter

from .views import (
    AnalyticsSnapshotViewSet,
    DashboardFilterViewSet,
    DashboardViewSet,
    DashboardWidgetViewSet,
    UserDashboardPreferenceViewSet,
)


app_name = "dashboard"


router = DefaultRouter()

router.register(
    "dashboards",
    DashboardViewSet,
    basename="dashboard",
)

router.register(
    "widgets",
    DashboardWidgetViewSet,
    basename="widget",
)

router.register(
    "preferences",
    UserDashboardPreferenceViewSet,
    basename="preference",
)

router.register(
    "filters",
    DashboardFilterViewSet,
    basename="filter",
)

router.register(
    "analytics-snapshots",
    AnalyticsSnapshotViewSet,
    basename="analytics-snapshot",
)


urlpatterns = router.urls