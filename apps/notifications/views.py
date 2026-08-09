from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.utils import timezone

from .models import (
    Notification,
    NotificationDeliveryAttempt,
    NotificationPreference,
    NotificationTemplate,
)

from .permissions import (
    CanManageNotifications,
    IsNotificationOwner,
)

from .serializers import (
    NotificationDeliveryAttemptSerializer,
    NotificationPreferenceSerializer,
    NotificationSerializer,
    NotificationTemplateSerializer,
)


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user

        queryset = (
            Notification.objects
            .select_related("user")
            .all()
            .order_by("-attempted_at")
        )

        if user.is_superuser:
            return queryset

        return queryset.filter(
            user=user
        )

    def get_permissions(self):
        if self.action in {
            "create",
            "update",
            "partial_update",
            "destroy",
        }:
            return [
                CanManageNotifications()
            ]

        return [
            IsNotificationOwner()
        ]

    @action(
        detail=True,
        methods=["post"],
        url_path="mark-read",
    )
    def mark_read(self, request, pk=None):
        notification = self.get_object()

        notification.read_at = timezone.now()

        notification.save(
            update_fields=[
                "read_at",
                "updated_at",
            ]
        )

        return Response(
            NotificationSerializer(
                notification
            ).data
        )


class NotificationTemplateViewSet(
    ModelViewSet
):
    queryset = (
        NotificationTemplate.objects
        .all()
        .order_by("name")
    )

    serializer_class = NotificationTemplateSerializer

    permission_classes = (
        CanManageNotifications,
    )


class NotificationDeliveryAttemptViewSet(
    ModelViewSet
):
    queryset = (
        NotificationDeliveryAttempt.objects
        .all()
        .order_by("-attempted_at")
    )

    serializer_class = (
        NotificationDeliveryAttemptSerializer
    )

    permission_classes = (
        CanManageNotifications,
    )


class NotificationPreferenceViewSet(
    ModelViewSet
):
    serializer_class = (
        NotificationPreferenceSerializer
    )

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return NotificationPreference.objects.all()

        return NotificationPreference.objects.filter(
            user=user
        )

    def get_permissions(self):
        if self.action in {
            "create",
            "update",
            "partial_update",
            "destroy",
        }:
            return [
                IsNotificationOwner()
            ]

        return [
            IsNotificationOwner()
        ]
