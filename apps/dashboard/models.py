import uuid

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel, Organization
from apps.users.models import User, UserRole


class DashboardType(models.TextChoices):
    ADMIN = "ADMIN", "Administrator Dashboard"
    DOCTOR = "DOCTOR", "Doctor Dashboard"
    PATIENT = "PATIENT", "Patient Dashboard"
    NURSE = "NURSE", "Nurse Dashboard"
    RADIOLOGIST = "RADIOLOGIST", "Radiologist Dashboard"
    LAB_TECHNICIAN = "LAB_TECHNICIAN", "Lab Technician Dashboard"
    STAFF = "STAFF", "Staff Dashboard"


class Dashboard(BaseModel):
    """
    Dashboard configuration.

    A dashboard defines a collection of widgets and their layout.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=150,
    )

    dashboard_type = models.CharField(
        max_length=30,
        choices=DashboardType.choices,
        db_index=True,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="dashboards",
    )

    description = models.TextField(
        blank=True,
    )

    is_default = models.BooleanField(
        default=False,
        db_index=True,
    )

    class Meta:
        db_table = "dashboards"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "name",
                ],
                name="unique_dashboard_name_per_org",
            ),
        ]
        indexes = [
            models.Index(
                fields=[
                    "dashboard_type",
                    "is_default",
                ],
                name="dashboard_type_default_idx",
            ),
        ]

    def __str__(self):
        return self.name


class WidgetType(models.TextChoices):
    STAT = "STAT", "Statistic"
    CHART = "CHART", "Chart"
    TABLE = "TABLE", "Table"
    CALENDAR = "CALENDAR", "Calendar"
    ACTIVITY = "ACTIVITY", "Activity"
    ALERT = "ALERT", "Alert"
    LIST = "LIST", "List"


class DashboardWidget(BaseModel):
    """
    Widget available on a dashboard.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    dashboard = models.ForeignKey(
        Dashboard,
        on_delete=models.CASCADE,
        related_name="widgets",
    )

    name = models.CharField(
        max_length=150,
    )

    widget_type = models.CharField(
        max_length=20,
        choices=WidgetType.choices,
    )

    component_key = models.CharField(
        max_length=150,
    )

    configuration = models.JSONField(
        default=dict,
        blank=True,
    )

    position_x = models.PositiveSmallIntegerField(
        default=0,
    )

    position_y = models.PositiveSmallIntegerField(
        default=0,
    )

    width = models.PositiveSmallIntegerField(
        default=4,
    )

    height = models.PositiveSmallIntegerField(
        default=3,
    )

    is_visible = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        db_table = "dashboard_widgets"
        ordering = [
            "position_y",
            "position_x",
        ]
        indexes = [
            models.Index(
                fields=[
                    "dashboard",
                    "is_visible",
                ],
                name="widget_dashboard_visible_idx",
            ),
        ]

    def clean(self):
        if self.width < 1 or self.height < 1:
            raise ValidationError(
                "Widget width and height must be greater than zero."
            )

    def __str__(self):
        return self.name


class UserDashboardPreference(BaseModel):
    """
    User-specific dashboard configuration.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="dashboard_preference",
    )

    default_dashboard = models.ForeignKey(
        Dashboard,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="users_using_as_default",
    )

    layout_configuration = models.JSONField(
        default=dict,
        blank=True,
    )

    compact_mode = models.BooleanField(
        default=False,
    )

    auto_refresh_enabled = models.BooleanField(
        default=True,
    )

    refresh_interval_seconds = models.PositiveIntegerField(
        default=60,
    )

    class Meta:
        db_table = "user_dashboard_preferences"

    def clean(self):
        if self.refresh_interval_seconds < 10:
            raise ValidationError(
                "Dashboard refresh interval cannot be less than 10 seconds."
            )

    def __str__(self):
        return self.user.email


class DashboardFilter(BaseModel):
    """
    Saved filter configuration for a dashboard.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="dashboard_filters",
    )

    dashboard = models.ForeignKey(
        Dashboard,
        on_delete=models.CASCADE,
        related_name="saved_filters",
    )

    name = models.CharField(
        max_length=150,
    )

    filters = models.JSONField(
        default=dict,
    )

    is_default = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "dashboard_filters"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "dashboard",
                    "name",
                ],
                name="unique_user_dashboard_filter",
            ),
        ]
        indexes = [
            models.Index(
                fields=[
                    "user",
                    "dashboard",
                    "is_default",
                ],
                name="dashboard_filter_default_idx",
            ),
        ]

    def __str__(self):
        return self.name


class AnalyticsSnapshotType(models.TextChoices):
    DAILY = "DAILY", "Daily"
    WEEKLY = "WEEKLY", "Weekly"
    MONTHLY = "MONTHLY", "Monthly"
    YEARLY = "YEARLY", "Yearly"


class AnalyticsSnapshot(BaseModel):
    """
    Persisted analytics snapshot.

    Used for dashboard/reporting workloads without repeatedly
    executing expensive aggregate queries against clinical tables.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="analytics_snapshots",
    )

    snapshot_type = models.CharField(
        max_length=20,
        choices=AnalyticsSnapshotType.choices,
        db_index=True,
    )

    snapshot_date = models.DateField(
        db_index=True,
    )

    metrics = models.JSONField(
        default=dict,
    )

    generated_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "analytics_snapshots"
        ordering = ["-snapshot_date"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "snapshot_type",
                    "snapshot_date",
                ],
                name="unique_analytics_snapshot",
            ),
        ]
        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "snapshot_type",
                    "snapshot_date",
                ],
                name="analytics_snapshot_lookup_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.organization.name} - "
            f"{self.snapshot_type} - "
            f"{self.snapshot_date}"
        )