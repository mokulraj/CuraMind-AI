from rest_framework import serializers

from .models import (
    AnalyticsSnapshot,
    Dashboard,
    DashboardFilter,
    DashboardWidget,
    UserDashboardPreference,
)


class DashboardWidgetSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = DashboardWidget
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class DashboardSerializer(serializers.ModelSerializer):
    widgets = DashboardWidgetSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Dashboard
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "widgets",
        )


class UserDashboardPreferenceSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = UserDashboardPreference
        fields = "__all__"
        read_only_fields = (
            "id",
            "user",
            "created_at",
            "updated_at",
        )


class DashboardFilterSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = DashboardFilter
        fields = "__all__"
        read_only_fields = (
            "id",
            "user",
            "created_at",
            "updated_at",
        )


class AnalyticsSnapshotSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = AnalyticsSnapshot
        fields = "__all__"
        read_only_fields = (
            "id",
            "generated_at",
            "created_at",
            "updated_at",
        )