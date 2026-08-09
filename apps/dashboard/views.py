from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import (
    AnalyticsSnapshot,
    Dashboard,
    DashboardFilter,
    DashboardWidget,
    UserDashboardPreference,
)

from .permissions import (
    CanAccessDashboard,
    CanManageDashboard,
)

from .serializers import (
    AnalyticsSnapshotSerializer,
    DashboardFilterSerializer,
    DashboardSerializer,
    DashboardWidgetSerializer,
    UserDashboardPreferenceSerializer,
)


class DashboardViewSet(ModelViewSet):
    queryset = (
        Dashboard.objects
        .prefetch_related("widgets")
        .all()
        .order_by("name")
    )

    serializer_class = DashboardSerializer

    permission_classes = (
        CanAccessDashboard,
    )

    def get_permissions(self):
        if self.action in {
            "create",
            "update",
            "partial_update",
            "destroy",
        }:
            return [
                CanManageDashboard()
            ]

        return [
            CanAccessDashboard()
        ]


class DashboardWidgetViewSet(ModelViewSet):
    queryset = (
        DashboardWidget.objects
        .all()
        .order_by(
            "position_y",
            "position_x",
        )
    )

    serializer_class = DashboardWidgetSerializer

    permission_classes = (
        CanAccessDashboard,
    )

    def get_permissions(self):
        if self.action in {
            "create",
            "update",
            "partial_update",
            "destroy",
        }:
            return [
                CanManageDashboard()
            ]

        return [
            CanAccessDashboard()
        ]


class UserDashboardPreferenceViewSet(
    ModelViewSet
):
    serializer_class = (
        UserDashboardPreferenceSerializer
    )

    permission_classes = (
        CanAccessDashboard,
    )

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return UserDashboardPreference.objects.all()

        return (
            UserDashboardPreference.objects
            .filter(user=user)
        )


class DashboardFilterViewSet(ModelViewSet):
    serializer_class = DashboardFilterSerializer

    permission_classes = (
        CanAccessDashboard,
    )

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return DashboardFilter.objects.all()

        return (
            DashboardFilter.objects
            .filter(user=user)
        )


class AnalyticsSnapshotViewSet(
    ModelViewSet
):
    queryset = (
        AnalyticsSnapshot.objects
        .all()
        .order_by("-snapshot_date")
    )

    serializer_class = AnalyticsSnapshotSerializer

    permission_classes = (
        CanAccessDashboard,
    )

    def get_permissions(self):
        if self.action in {
            "create",
            "update",
            "partial_update",
            "destroy",
        }:
            return [
                CanManageDashboard()
            ]

        return [
            CanAccessDashboard()
        ]