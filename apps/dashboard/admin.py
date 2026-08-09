from django.contrib import admin

from .models import (
    AnalyticsSnapshot,
    Dashboard,
    DashboardFilter,
    DashboardWidget,
    UserDashboardPreference,
)


class DashboardWidgetInline(admin.TabularInline):
    model = DashboardWidget
    extra = 0


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "dashboard_type",
        "organization",
        "is_default",
    )
    list_filter = (
        "dashboard_type",
        "is_default",
        "organization",
    )
    search_fields = (
        "name",
        "description",
        "organization__name",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    inlines = [
        DashboardWidgetInline,
    ]


@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "dashboard",
        "widget_type",
        "component_key",
        "is_visible",
    )
    list_filter = (
        "widget_type",
        "is_visible",
    )
    search_fields = (
        "name",
        "component_key",
        "dashboard__name",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(UserDashboardPreference)
class UserDashboardPreferenceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "default_dashboard",
        "compact_mode",
        "auto_refresh_enabled",
        "refresh_interval_seconds",
    )
    list_filter = (
        "compact_mode",
        "auto_refresh_enabled",
    )
    search_fields = (
        "user__email",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(DashboardFilter)
class DashboardFilterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "dashboard",
        "is_default",
    )
    list_filter = (
        "is_default",
        "dashboard",
    )
    search_fields = (
        "name",
        "user__email",
        "dashboard__name",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(AnalyticsSnapshot)
class AnalyticsSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "snapshot_type",
        "snapshot_date",
        "generated_at",
    )
    list_filter = (
        "snapshot_type",
        "organization",
    )
    search_fields = (
        "organization__name",
    )
    date_hierarchy = "snapshot_date"
    readonly_fields = (
        "id",
        "generated_at",
        "created_at",
        "updated_at",
    )