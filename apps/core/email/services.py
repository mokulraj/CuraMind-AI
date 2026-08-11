from django.conf import settings
from django.core.mail import (
    EmailMultiAlternatives,
)

from apps.core.email.validators import (
    validate_recipient_email,
    validate_sender_email,
    validate_subject,
)


class EmailService:
    def __init__(
        self,
    ):
        self.from_email = (
            settings.DEFAULT_FROM_EMAIL
        )

        validate_sender_email(
            self.from_email
        )

    def send(
        self,
        *,
        recipient,
        subject,
        text_content,
        html_content=None,
        reply_to=None,
    ):
        recipient = (
            validate_recipient_email(
                recipient
            )
        )

        subject = (
            validate_subject(
                subject
            )
        )

        if not text_content:
            raise ValueError(
                "Plain-text email content is required."
            )

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=self.from_email,
            to=[recipient],
            reply_to=(
                [reply_to]
                if reply_to
                else None
            ),
        )

        if html_content:
            email.attach_alternative(
                html_content,
                "text/html",
            )

        return email.send(
            fail_silently=False
        )


def send_email(
    *,
    recipient,
    subject,
    text_content,
    html_content=None,
    reply_to=None,
):
    service = EmailService()

    return service.send(
        recipient=recipient,
        subject=subject,
        text_content=text_content,
        html_content=html_content,
        reply_to=reply_to,
    )