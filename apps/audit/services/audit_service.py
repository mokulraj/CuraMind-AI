from apps.audit.models import AuditEvent


class AuditService:
    """
    Centralized audit-event creation.
    """

    @staticmethod
    def record_event(
        *,
        actor=None,
        event_type,
        category,
        severity,
        action,
        description="",
        target_model="",
        target_object_id="",
        target_display="",
        request_id="",
        ip_address=None,
        user_agent="",
        endpoint="",
        http_method="",
        response_status=None,
        metadata=None,
        old_values=None,
        new_values=None,
    ):
        return AuditEvent.objects.create(
            actor=actor,
            event_type=event_type,
            category=category,
            severity=severity,
            action=action,
            description=description,
            target_model=target_model,
            target_object_id=target_object_id,
            target_display=target_display,
            request_id=request_id,
            ip_address=ip_address,
            user_agent=user_agent,
            endpoint=endpoint,
            http_method=http_method,
            response_status=response_status,
            metadata=metadata or {},
            old_values=old_values or {},
            new_values=new_values or {},
        )