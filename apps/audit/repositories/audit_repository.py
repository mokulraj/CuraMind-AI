from apps.audit.models import (
    AuditEvent,
    AuthenticationEvent,
    PatientDataAccessLog,
    SecurityEvent,
)


class AuditRepository:
    """
    Read-oriented database access for audit records.
    """

    @staticmethod
    def get_event_by_id(
        event_id,
    ):
        return (
            AuditEvent.objects
            .select_related("actor")
            .filter(pk=event_id)
            .first()
        )

    @staticmethod
    def list_events_for_actor(
        actor_id,
    ):
        return (
            AuditEvent.objects
            .filter(
                actor_id=actor_id
            )
            .order_by("-created_at")
        )

    @staticmethod
    def list_patient_access_logs(
        patient_id,
    ):
        return (
            PatientDataAccessLog.objects
            .select_related(
                "patient",
                "accessed_by",
            )
            .filter(
                patient_id=patient_id
            )
            .order_by("-created_at")
        )

    @staticmethod
    def list_authentication_events(
        user_id=None,
    ):
        queryset = AuthenticationEvent.objects.all()

        if user_id:
            queryset = queryset.filter(
                user_id=user_id
            )

        return queryset.order_by(
            "-created_at"
        )

    @staticmethod
    def list_security_events(
        unresolved_only=False,
    ):
        queryset = SecurityEvent.objects.all()

        if unresolved_only:
            queryset = queryset.filter(
                resolved=False
            )

        return queryset.order_by(
            "-created_at"
        )