from django.db import transaction

from apps.notifications.models import Notification


class NotificationService:
    """
    Creates application notifications.

    Actual email/SMS/push delivery is handled separately.
    """

    @staticmethod
    @transaction.atomic
    def create_notification(
        *,
        user,
        title,
        message,
        notification_type,
        channel,
        priority=None,
        metadata=None,
    ):
        return Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            channel=channel,
            priority=priority,
            metadata=metadata or {},
        )

    @staticmethod
    @transaction.atomic
    def mark_as_read(
        *,
        notification,
    ):
        if hasattr(notification, "is_read"):
            notification.is_read = True

        if hasattr(notification, "read_at"):
            from django.utils import timezone

            notification.read_at = timezone.now()

        update_fields = [
            "updated_at",
        ]

        if hasattr(notification, "is_read"):
            update_fields.append("is_read")

        if hasattr(notification, "read_at"):
            update_fields.append("read_at")

        notification.save(
            update_fields=update_fields
        )

        return notification