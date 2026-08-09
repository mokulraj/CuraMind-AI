from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import (
    AuditEvent,
    AuthenticationEvent,
    PatientDataAccessLog,
    SecurityEvent,
)

from .permissions import (
    AuditReadOnly,
    CanReadAuditLogs,
)

from .serializers import (
    AuditEventSerializer,
    AuthenticationEventSerializer,
    PatientDataAccessLogSerializer,
    SecurityEventSerializer,
)


class AuditEventViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = (
        AuditEvent.objects
        .select_related("actor")
        .all()
        .order_by("-created_at")
    )

    serializer_class = AuditEventSerializer

    permission_classes = (
        CanReadAuditLogs,
        AuditReadOnly,
    )


class AuthenticationEventViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = (
        AuthenticationEvent.objects
        .all()
        .order_by("-created_at")
    )

    serializer_class = AuthenticationEventSerializer

    permission_classes = (
        CanReadAuditLogs,
        AuditReadOnly,
    )


class PatientDataAccessLogViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = (
        PatientDataAccessLog.objects
        .select_related(
            "patient",
            "accessed_by",
        )
        .all()
        .order_by("-created_at")
    )

    serializer_class = PatientDataAccessLogSerializer

    permission_classes = (
        CanReadAuditLogs,
        AuditReadOnly,
    )


class SecurityEventViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = (
        SecurityEvent.objects
        .all()
        .order_by("-created_at")
    )

    serializer_class = SecurityEventSerializer

    permission_classes = (
        CanReadAuditLogs,
        AuditReadOnly,
    )