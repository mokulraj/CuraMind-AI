from collections.abc import Mapping, Sequence
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from uuid import UUID

from django.core.files import File

from apps.audit.models import AuditEvent


SENSITIVE_KEYS = {
    "password",
    "passwd",
    "secret",
    "token",
    "access_token",
    "refresh_token",
    "id_token",
    "authorization",
    "api_key",
    "apikey",
    "private_key",
    "client_secret",
    "secret_key",
}


REDACTED_VALUE = "[REDACTED]"


def sanitize_value(value):
    """
    Recursively sanitize sensitive values before they are
    stored in audit logs.
    """

    if isinstance(value, Mapping):
        sanitized = {}

        for key, item in value.items():
            key_string = str(key)

            if key_string.lower() in SENSITIVE_KEYS:
                sanitized[key_string] = REDACTED_VALUE
            else:
                sanitized[key_string] = sanitize_value(item)

        return sanitized

    if isinstance(value, (list, tuple, set)):
        return [
            sanitize_value(item)
            for item in value
        ]

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    if isinstance(value, UUID):
        return str(value)

    if isinstance(value, Decimal):
        return str(value)

    if isinstance(value, Path):
        return str(value)

    if isinstance(value, File):
        return {
            "name": value.name,
            "size": getattr(
                value,
                "size",
                None,
            ),
        }

    if isinstance(
        value,
        (str, int, float, bool),
    ):
        return value

    if value is None:
        return None

    return str(value)


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
            metadata=sanitize_value(
                metadata or {}
            ),
            old_values=sanitize_value(
                old_values or {}
            ),
            new_values=sanitize_value(
                new_values or {}
            ),
        )


__all__ = [
    "AuditService",
    "sanitize_value",
]