from django.contrib import admin

from .models import (
    AuditEvent,
    AuthenticationEvent,
    PatientDataAccessLog,
    SecurityEvent,
)


# ============================================================
# AUDIT EVENT
# ============================================================


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "event_type",
        "category",
        "severity",
        "action",
        "target_model",
        "target_object_id",
        "actor",
    )

    list_filter = (
        "event_type",
        "category",
        "severity",
        "created_at",
    )

    search_fields = (
        "event_id",
        "action",
        "description",
        "target_model",
        "target_object_id",
        "target_display",
        "request_id",
        "ip_address",
    )

    readonly_fields = (
        "id",
        "event_id",
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
        "actor",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 50

    def has_add_permission(
        self,
        request,
    ):
        return False

    def has_change_permission(
        self,
        request,
        obj=None,
    ):
        return False

    def has_delete_permission(
        self,
        request,
        obj=None,
    ):
        return False


# ============================================================
# AUTHENTICATION EVENT
# ============================================================


@admin.register(AuthenticationEvent)
class AuthenticationEventAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "event_type",
        "email_attempted",
        "success",
        "user",
        "ip_address",
    )

    list_filter = (
        "event_type",
        "success",
        "created_at",
    )

    search_fields = (
        "email_attempted",
        "request_id",
        "ip_address",
        "failure_reason",
    )

    readonly_fields = (
        "id",
        "email_attempted",
        "event_type",
        "success",
        "ip_address",
        "user_agent",
        "request_id",
        "failure_reason",
        "metadata",
        "user",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 50

    def has_add_permission(
        self,
        request,
    ):
        return False

    def has_change_permission(
        self,
        request,
        obj=None,
    ):
        return False

    def has_delete_permission(
        self,
        request,
        obj=None,
    ):
        return False


# ============================================================
# PATIENT DATA ACCESS LOG
# ============================================================


@admin.register(PatientDataAccessLog)
class PatientDataAccessLogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "access_type",
        "patient",
        "accessed_by",
        "resource_type",
        "resource_id",
    )

    list_filter = (
        "access_type",
        "created_at",
    )

    search_fields = (
        "resource_type",
        "resource_id",
        "purpose",
        "request_id",
        "ip_address",
    )

    readonly_fields = (
        "id",
        "access_type",
        "resource_type",
        "resource_id",
        "purpose",
        "ip_address",
        "user_agent",
        "request_id",
        "accessed_by",
        "patient",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 50

    def has_add_permission(
        self,
        request,
    ):
        return False

    def has_change_permission(
        self,
        request,
        obj=None,
    ):
        return False

    def has_delete_permission(
        self,
        request,
        obj=None,
    ):
        return False


# ============================================================
# SECURITY EVENT
# ============================================================


@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "event_type",
        "severity",
        "resolved",
        "user",
        "ip_address",
    )

    list_filter = (
        "event_type",
        "severity",
        "resolved",
        "created_at",
    )

    search_fields = (
        "description",
        "request_id",
        "ip_address",
        "endpoint",
    )

    readonly_fields = (
        "id",
        "event_type",
        "severity",
        "description",
        "ip_address",
        "user_agent",
        "endpoint",
        "request_id",
        "metadata",
        "resolved",
        "resolved_at",
        "resolved_by",
        "user",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 50

    def has_add_permission(
        self,
        request,
    ):
        return False

    def has_change_permission(
        self,
        request,
        obj=None,
    ):
        return False

    def has_delete_permission(
        self,
        request,
        obj=None,
    ):
        return False