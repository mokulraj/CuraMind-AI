from apps.notifications.models import (
    Notification,
    NotificationDeliveryAttempt,
    NotificationPreference,
    NotificationTemplate,
)


class NotificationRepository:
    """
    Database access for notifications.
    """

    @staticmethod
    def get_by_id(
        notification_id,
    ):
        return (
            Notification.objects
            .select_related("user")
            .filter(pk=notification_id)
            .first()
        )

    @staticmethod
    def list_for_user(
        user_id,
        unread_only=False,
    ):
        queryset = Notification.objects.filter(
            user_id=user_id
        )

        if unread_only:
            queryset = queryset.filter(
                read_at__isnull=True
            )

        return queryset.order_by(
            "-created_at"
        )

    @staticmethod
    def get_preference(
        user_id,
    ):
        return (
            NotificationPreference.objects
            .filter(
                user_id=user_id
            )
            .first()
        )

    @staticmethod
    def get_template(
        *,
        notification_type,
        channel,
    ):
        return (
            NotificationTemplate.objects
            .filter(
                notification_type=notification_type,
                channel=channel,
                is_active=True,
            )
            .order_by("-created_at")
            .first()
        )

    @staticmethod
    def list_delivery_attempts(
        notification_id,
    ):
        return (
            NotificationDeliveryAttempt.objects
            .filter(
                notification_id=notification_id
            )
            .order_by("-attempt_number")
        )