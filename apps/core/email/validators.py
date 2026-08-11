from email.utils import parseaddr

from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def validate_recipient_email(
    email,
):
    if not email:
        raise ValidationError(
            "Recipient email address is required."
        )

    email = email.strip()

    try:
        validate_email(
            email
        )
    except ValidationError as exc:
        raise ValidationError(
            "Invalid recipient email address."
        ) from exc

    return email


def validate_subject(
    subject,
):
    if not subject:
        raise ValidationError(
            "Email subject is required."
        )

    subject = subject.strip()

    if not subject:
        raise ValidationError(
            "Email subject cannot be empty."
        )

    if len(subject) > 998:
        raise ValidationError(
            "Email subject is too long."
        )

    if "\r" in subject or "\n" in subject:
        raise ValidationError(
            "Email subject contains invalid characters."
        )

    return subject


def validate_sender_email(
    email,
):
    if not email:
        raise ValidationError(
            "Sender email address is required."
        )

    email = email.strip()

    display_name, email_address = parseaddr(
        email
    )

    if not email_address:
        raise ValidationError(
            "Invalid sender email address."
        )

    try:
        validate_email(
            email_address
        )
    except ValidationError as exc:
        raise ValidationError(
            "Invalid sender email address."
        ) from exc

    return email