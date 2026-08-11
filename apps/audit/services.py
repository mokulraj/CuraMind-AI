import uuid

from django.core.exceptions import ValidationError

from apps.audit.models import (
    AuditEvent,
    AuditEventType,
    AuditSeverity,
)


SENSITIVE_KEYS = {
    "password",
    "password_hash",
    "token",
    "access_token",
    "refresh_token",
    "authorization",
    "secret",
    "api_key",
    "private_key",
    "credit_card",
    "card_number",
    "cvv",
    "otp",
}


def sanitize_value(
    value,
):
    if isinstance(
        value,
        dict,
    ):
        return {
            str(key): sanitize_value(
                item
            )
            for key, item in value.items()
            if str(key).lower()
            not in SENSITIVE_KEYS
        }

    if isinstance(
        value,
        list,
    ):
        return [
            sanitize_value(item)
            for item in value
        ]

    if isinstance(
        value,
        tuple,
    ):
        return [
            sanitize_value(item)
            for item in value
        ]

    if isinstance(
        value,
        uuid.UUID,
    ):
        return str(value)

    if isinstance(
        value,
        bytes,
    ):
        return "<binary-data>"

    return value


def get_client_ip(
    request,
):
    if request is None:
        return None

    forwarded_for = request.META.get(
        "HTTP_X_FORWARDED_FOR"
    )

    if forwarded_for:
        return (
            forwarded_for
            .split(",")[0]
            .strip()
        )

    return request.META.get(
        "REMOTE_ADDR"
    )


def get_actor_identifier(
    actor,
):
    if actor is None:
        return ""

    if hasattr(
        actor,
        "get_username",
    ):
        return actor.get_username()

    return str(
        getattr(
            actor,
            "pk",
            "",
        )
    )


def create_audit_event(
    *,
    event_type,
    action,
    actor=None,
    severity=AuditSeverity.INFO,
    description="",
    instance=None,
    request=None,
    before_data=None,
    after_data=None,
    metadata=None,
    success=True,
):
    if event_type not in {
        choice[0]
        for choice
        in AuditEventType.choices
    }:
        raise ValidationError(
            "Invalid audit event type."
        )

    if severity not in {
        choice[0]
        for choice
        in AuditSeverity.choices
    }:
        raise ValidationError(
            "Invalid audit severity."
        )

    app_label = ""

    model_name = ""

    object_id = ""

    object_repr = ""

    if instance is not None:
        meta = instance._meta

        app_label = meta.app_label

        model_name = meta.model_name

        object_id = str(
            getattr(
                instance,
                "pk",
                "",
            )
        )

        object_repr = str(
            instance
        )[:500]

    request_id = None

    ip_address = None

    user_agent = ""

    request_method = ""

    request_path = ""

    if request is not None:
        request_id = getattr(
            request,
            "audit_request_id",
            None,
        )

        ip_address = get_client_ip(
            request
        )

        user_agent = request.META.get(
            "HTTP_USER_AGENT",
            "",
        )[:1000]

        request_method = request.method

        request_path = request.path[:2000]

    return AuditEvent.objects.create(
        event_type=event_type,
        severity=severity,
        actor=actor,
        actor_identifier=(
            get_actor_identifier(
                actor
            )
        ),
        action=action,
        description=description,
        app_label=app_label,
        model_name=model_name,
        object_id=object_id,
        object_repr=object_repr,
        request_id=request_id,
        ip_address=ip_address,
        user_agent=user_agent,
        request_method=request_method,
        request_path=request_path,
        before_data=sanitize_value(
            before_data
        ),
        after_data=sanitize_value(
            after_data
        ),
        metadata=sanitize_value(
            metadata or {}
        ),
        success=success,
    )