from rest_framework import serializers

from .models import (
    Notification,
    NotificationDeliveryAttempt,
    NotificationPreference,
    NotificationTemplate,
)


class NotificationTemplateSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = NotificationTemplate
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "sent_at",
            "delivered_at",
            "read_at",
            "failure_reason",
        )


class NotificationDeliveryAttemptSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = NotificationDeliveryAttempt
        fields = "__all__"
        read_only_fields = "__all__"


class NotificationPreferenceSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = NotificationPreference
        fields = "__all__"
        read_only_fields = (
            "id",
            "user",
            "created_at",
            "updated_at",
        )