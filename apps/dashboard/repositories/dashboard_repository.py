from apps.dashboard.models import (
    AnalyticsSnapshot,
    Dashboard,
    DashboardFilter,
    DashboardWidget,
    UserDashboardPreference,
)


class DashboardRepository:
    """
    Database access for dashboards.
    """

    @staticmethod
    def get_dashboard_by_id(
        dashboard_id,
    ):
        return (
            Dashboard.objects
            .prefetch_related("widgets")
            .filter(pk=dashboard_id)
            .first()
        )

    @staticmethod
    def list_dashboards(
        *,
        organization_id=None,
        dashboard_type=None,
    ):
        queryset = Dashboard.objects.all()

        if organization_id:
            queryset = queryset.filter(
                organization_id=organization_id
            )

        if dashboard_type:
            queryset = queryset.filter(
                dashboard_type=dashboard_type
            )

        return queryset.order_by("name")

    @staticmethod
    def list_widgets(
        dashboard_id,
        visible_only=True,
    ):
        queryset = DashboardWidget.objects.filter(
            dashboard_id=dashboard_id
        )

        if visible_only:
            queryset = queryset.filter(
                is_visible=True
            )

        return queryset.order_by(
            "position_y",
            "position_x",
        )

    @staticmethod
    def get_user_preference(
        user_id,
    ):
        return (
            UserDashboardPreference.objects
            .select_related(
                "default_dashboard",
            )
            .filter(
                user_id=user_id
            )
            .first()
        )

    @staticmethod
    def list_user_filters(
        *,
        user_id,
        dashboard_id,
    ):
        return (
            DashboardFilter.objects
            .filter(
                user_id=user_id,
                dashboard_id=dashboard_id,
            )
            .order_by(
                "-is_default",
                "name",
            )
        )

    @staticmethod
    def get_latest_snapshot(
        *,
        organization_id,
        snapshot_type,
    ):
        return (
            AnalyticsSnapshot.objects
            .filter(
                organization_id=organization_id,
                snapshot_type=snapshot_type,
            )
            .order_by("-snapshot_date")
            .first()
        )