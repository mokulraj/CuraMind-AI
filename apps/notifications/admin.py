from django.contrib import admin

from .models import (
    Notification,
    NotificationDeliveryAttempt,
    NotificationPreference,
    NotificationTemplate,
)


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "notification_type",
        "channel",
        "is_active",
    )
    list_filter = (
        "notification_type",
        "channel",
        "is_active",
    )
    search_fields = (
        "name",
        "subject_template",
        "body_template",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "title",
        "notification_type",
        "channel",
        "priority",
        "status",
        "created_at",
    )
    list_filter = (
        "notification_type",
        "channel",
        "priority",
        "status",
    )
    search_fields = (
        "user__email",
        "title",
        "message",
    )
    date_hierarchy = "created_at"
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(NotificationDeliveryAttempt)
class NotificationDeliveryAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "notification",
        "attempt_number",
        "status",
        "provider_name",
        "attempted_at",
    )
    list_filter = (
        "status",
        "provider_name",
    )
    search_fields = (
        "notification__user__email",
        "provider_message_id",
    )
    readonly_fields = (
        "id",
        "attempted_at",
    )


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "email_enabled",
        "sms_enabled",
        "push_enabled",
        "in_app_enabled",
    )
    list_filter = (
        "email_enabled",
        "sms_enabled",
        "push_enabled",
        "in_app_enabled",
    )
    search_fields = (
        "user__email",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )