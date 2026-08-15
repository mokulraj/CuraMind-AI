import uuid

from django.conf import settings
from django.db import models


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        APPOINTMENT_CREATED = (
            "APPOINTMENT_CREATED",
            "Appointment Created",
        )
        APPOINTMENT_CONFIRMED = (
            "APPOINTMENT_CONFIRMED",
            "Appointment Confirmed",
        )
        APPOINTMENT_REMINDER = (
            "APPOINTMENT_REMINDER",
            "Appointment Reminder",
        )
        APPOINTMENT_CANCELLED = (
            "APPOINTMENT_CANCELLED",
            "Appointment Cancelled",
        )
        APPOINTMENT_RESCHEDULED = (
            "APPOINTMENT_RESCHEDULED",
            "Appointment Rescheduled",
        )
        MEDICAL_REPORT_READY = (
            "MEDICAL_REPORT_READY",
            "Medical Report Ready",
        )
        IMAGING_REPORT_READY = (
            "IMAGING_REPORT_READY",
            "Imaging Report Ready",
        )
        AI_ANALYSIS_COMPLETED = (
            "AI_ANALYSIS_COMPLETED",
            "AI Analysis Completed",
        )
        AI_REVIEW_REQUIRED = (
            "AI_REVIEW_REQUIRED",
            "AI Review Required",
        )
        PAYMENT_SUCCESS = (
            "PAYMENT_SUCCESS",
            "Payment Successful",
        )
        PAYMENT_FAILED = (
            "PAYMENT_FAILED",
            "Payment Failed",
        )
        PASSWORD_CHANGED = (
            "PASSWORD_CHANGED",
            "Password Changed",
        )
        SECURITY_ALERT = (
            "SECURITY_ALERT",
            "Security Alert",
        )
        SYSTEM = (
            "SYSTEM",
            "System Notification",
        )

    class Channel(models.TextChoices):
        IN_APP = "IN_APP", "In-App"
        EMAIL = "EMAIL", "Email"
        SMS = "SMS", "SMS"
        PUSH = "PUSH", "Push Notification"

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        NORMAL = "NORMAL", "Normal"
        HIGH = "HIGH", "High"
        URGENT = "URGENT", "Urgent"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        QUEUED = "QUEUED", "Queued"
        SENDING = "SENDING", "Sending"
        SENT = "SENT", "Sent"
        DELIVERED = "DELIVERED", "Delivered"
        READ = "READ", "Read"
        FAILED = "FAILED", "Failed"
        CANCELLED = "CANCELLED", "Cancelled"

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    notification_type = models.CharField(
        max_length=50,
        choices=NotificationType.choices,
        db_index=True,
    )

    channel = models.CharField(
        max_length=20,
        choices=Channel.choices,
        db_index=True,
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default="NORMAL",
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default="PENDING",
        db_index=True,
    )

    title = models.CharField(
        max_length=255,
    )

    message = models.TextField()

    action_url = models.URLField(
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    scheduled_for = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    read_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    failure_reason = models.TextField(
        blank=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    template = models.ForeignKey(
        "NotificationTemplate",
        on_delete=models.PROTECT,
        related_name="notifications",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "notifications"
        ordering = [
            "-created_at",
        ]
        indexes = [
            models.Index(
                fields=[
                    "user",
                    "status",
                    "created_at",
                ],
                name="notification_user_status_idx",
            ),
            models.Index(
                fields=[
                    "channel",
                    "status",
                    "scheduled_for",
                ],
                name="notification_delivery_idx",
            ),
            models.Index(
                fields=[
                    "notification_type",
                    "created_at",
                ],
                name="notification_type_date_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.user} - {self.title}"
        )


class NotificationDeliveryAttempt(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        QUEUED = "QUEUED", "Queued"
        SENDING = "SENDING", "Sending"
        SENT = "SENT", "Sent"
        DELIVERED = "DELIVERED", "Delivered"
        READ = "READ", "Read"
        FAILED = "FAILED", "Failed"
        CANCELLED = "CANCELLED", "Cancelled"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name="delivery_attempts",
    )

    attempt_number = models.PositiveSmallIntegerField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        db_index=True,
    )

    provider_name = models.CharField(
        max_length=100,
        blank=True,
    )

    provider_message_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    response_code = models.CharField(
        max_length=100,
        blank=True,
    )

    response_message = models.TextField(
        blank=True,
    )

    attempted_at = models.DateTimeField(
        auto_now_add=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "notification_delivery_attempts"
        ordering = [
            "-attempted_at",
        ]
        indexes = [
            models.Index(
                fields=[
                    "notification",
                    "attempted_at",
                ],
                name="notification_attempt_date_idx",
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "notification",
                    "attempt_number",
                ],
                name="unique_notification_attempt",
            ),
        ]

    def __str__(self):
        return (
            f"{self.notification} - "
            f"Attempt {self.attempt_number}"
        )


class NotificationPreference(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_preferences",
    )

    email_enabled = models.BooleanField(
        default=True,
    )

    sms_enabled = models.BooleanField(
        default=True,
    )

    push_enabled = models.BooleanField(
        default=True,
    )

    in_app_enabled = models.BooleanField(
        default=True,
    )

    appointment_reminders_enabled = models.BooleanField(
        default=True,
    )

    marketing_enabled = models.BooleanField(
        default=False,
    )

    security_alerts_enabled = models.BooleanField(
        default=True,
    )

    clinical_notifications_enabled = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "notification_preferences"

    def __str__(self):
        return (
            f"Notification preferences - "
            f"{self.user.email}"
        )


class NotificationTemplate(models.Model):

    class NotificationType(models.TextChoices):
        APPOINTMENT_CREATED = (
            "APPOINTMENT_CREATED",
            "Appointment Created",
        )
        APPOINTMENT_CONFIRMED = (
            "APPOINTMENT_CONFIRMED",
            "Appointment Confirmed",
        )
        APPOINTMENT_REMINDER = (
            "APPOINTMENT_REMINDER",
            "Appointment Reminder",
        )
        APPOINTMENT_CANCELLED = (
            "APPOINTMENT_CANCELLED",
            "Appointment Cancelled",
        )
        APPOINTMENT_RESCHEDULED = (
            "APPOINTMENT_RESCHEDULED",
            "Appointment Rescheduled",
        )
        MEDICAL_REPORT_READY = (
            "MEDICAL_REPORT_READY",
            "Medical Report Ready",
        )
        IMAGING_REPORT_READY = (
            "IMAGING_REPORT_READY",
            "Imaging Report Ready",
        )
        AI_ANALYSIS_COMPLETED = (
            "AI_ANALYSIS_COMPLETED",
            "AI Analysis Completed",
        )
        AI_REVIEW_REQUIRED = (
            "AI_REVIEW_REQUIRED",
            "AI Review Required",
        )
        PAYMENT_SUCCESS = (
            "PAYMENT_SUCCESS",
            "Payment Successful",
        )
        PAYMENT_FAILED = (
            "PAYMENT_FAILED",
            "Payment Failed",
        )
        PASSWORD_CHANGED = (
            "PASSWORD_CHANGED",
            "Password Changed",
        )
        SECURITY_ALERT = (
            "SECURITY_ALERT",
            "Security Alert",
        )
        SYSTEM = (
            "SYSTEM",
            "System Notification",
        )

    class Channel(models.TextChoices):
        IN_APP = "IN_APP", "In-App"
        EMAIL = "EMAIL", "Email"
        SMS = "SMS", "SMS"
        PUSH = "PUSH", "Push Notification"

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
    )

    notification_type = models.CharField(
        max_length=50,
        choices=NotificationType.choices,
        db_index=True,
    )

    channel = models.CharField(
        max_length=20,
        choices=Channel.choices,
        db_index=True,
    )

    subject_template = models.CharField(
        max_length=500,
        blank=True,
    )

    body_template = models.TextField()

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        db_table = "notification_templates"
        indexes = [
            models.Index(
                fields=[
                    "notification_type",
                    "channel",
                    "is_active",
                ],
                name="notif_template_lookup_idx",
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "notification_type",
                    "channel",
                    "name",
                ],
                name="unique_notification_template",
            ),
        ]

    def __str__(self):
        return self.name