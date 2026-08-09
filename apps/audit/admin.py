from django.contrib import admin

from .models import (
    AuditEvent,
    AuthenticationEvent,
    PatientDataAccessLog,
    SecurityEvent,
)


class ImmutableAuditAdmin(admin.ModelAdmin):
    """
    Prevent modification and deletion of audit records from
    Django Admin.
    """

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AuditEvent)
class AuditEventAdmin(ImmutableAuditAdmin):
    list_display = (
        "event_id",
        "actor",
        "event_type",
        "category",
        "severity",
        "action",
        "created_at",
    )
    list_filter = (
        "event_type",
        "category",
        "severity",
    )
    search_fields = (
        "event_id",
        "action",
        "description",
        "request_id",
        "target_model",
        "target_object_id",
        "ip_address",
    )
    date_hierarchy = "created_at"
    readonly_fields = (
        "event_id",
        "actor",
        "event_type",
        "category",
        "severity",
        "action",
        "description",
        "target_model",
        "target_object_id",
        "target_display",
        "request_id",
        "ip_address",
        "user_agent",
        "endpoint",
        "http_method",
        "response_status",
        "metadata",
        "old_values",
        "new_values",
        "created_at",
    )


@admin.register(AuthenticationEvent)
class AuthenticationEventAdmin(ImmutableAuditAdmin):
    list_display = (
        "user",
        "email_attempted",
        "event_type",
        "success",
        "ip_address",
        "created_at",
    )
    list_filter = (
        "event_type",
        "success",
    )
    search_fields = (
        "email_attempted",
        "ip_address",
        "request_id",
    )
    date_hierarchy = "created_at"
    readonly_fields = (
        "id",
        "user",
        "email_attempted",
        "event_type",
        "success",
        "ip_address",
        "user_agent",
        "request_id",
        "failure_reason",
        "metadata",
        "created_at",
    )


@admin.register(PatientDataAccessLog)
class PatientDataAccessLogAdmin(ImmutableAuditAdmin):
    list_display = (
        "patient",
        "accessed_by",
        "access_type",
        "resource_type",
        "resource_id",
        "created_at",
    )
    list_filter = (
        "access_type",
        "resource_type",
    )
    search_fields = (
        "patient__user__email",
        "accessed_by__email",
        "resource_type",
        "resource_id",
        "request_id",
    )
    date_hierarchy = "created_at"
    readonly_fields = (
        "id",
        "patient",
        "accessed_by",
        "access_type",
        "resource_type",
        "resource_id",
        "purpose",
        "ip_address",
        "user_agent",
        "request_id",
        "created_at",
    )


@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = (
        "event_type",
        "severity",
        "user",
        "resolved",
        "resolved_by",
        "created_at",
    )
    list_filter = (
        "event_type",
        "severity",
        "resolved",
    )
    search_fields = (
        "description",
        "ip_address",
        "request_id",
        "user__email",
    )
    date_hierarchy = "created_at"
    readonly_fields = (
        "id",
        "created_at",
    )