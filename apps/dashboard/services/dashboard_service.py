from django.db import transaction

from apps.dashboard.models import (
    Dashboard,
    UserDashboardPreference,
)


class DashboardService:
    """
    Dashboard configuration operations.
    """

    @staticmethod
    def get_user_dashboard(
        *,
        user,
    ):
        preference = (
            UserDashboardPreference.objects
            .select_related("default_dashboard")
            .filter(user=user)
            .first()
        )

        if preference and preference.default_dashboard:
            return preference.default_dashboard

        return (
            Dashboard.objects
            .filter(is_default=True)
            .order_by("name")
            .first()
        )

    @staticmethod
    @transaction.atomic
    def set_default_dashboard(
        *,
        user,
        dashboard,
    ):
        preference, _ = (
            UserDashboardPreference.objects
            .select_for_update()
            .get_or_create(
                user=user,
            )
        )

        preference.default_dashboard = dashboard

        preference.save(
            update_fields=[
                "default_dashboard",
                "updated_at",
            ]
        )

        return preference