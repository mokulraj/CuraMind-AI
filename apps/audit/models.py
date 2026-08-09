import uuid

from django.core.exceptions import ValidationError
from django.db import models


class AuditEventType(models.TextChoices):
    CREATE = "CREATE", "Create"
    READ = "READ", "Read"
    UPDATE = "UPDATE", "Update"
    DELETE = "DELETE", "Delete"

    LOGIN = "LOGIN", "Login"
    LOGOUT = "LOGOUT", "Logout"
    LOGIN_FAILED = "LOGIN_FAILED", "Login Failed"

    EXPORT = "EXPORT", "Export"
    DOWNLOAD = "DOWNLOAD", "Download"
    UPLOAD = "UPLOAD", "Upload"

    APPROVE = "APPROVE", "Approve"
    REJECT = "REJECT", "Reject"

    AI_INFERENCE = "AI_INFERENCE", "AI Inference"
    AI_REVIEW = "AI_REVIEW", "AI Review"

    PASSWORD_CHANGE = "PASSWORD_CHANGE", "Password Change"
    PASSWORD_RESET = "PASSWORD_RESET", "Password Reset"

    PERMISSION_CHANGE = "PERMISSION_CHANGE", "Permission Change"

    SECURITY_EVENT = "SECURITY_EVENT", "Security Event"


class AuditSeverity(models.TextChoices):
    INFO = "INFO", "Information"
    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGH = "HIGH", "High"
    CRITICAL = "CRITICAL", "Critical"


class AuditCategory(models.TextChoices):
    AUTHENTICATION = "AUTHENTICATION", "Authentication"
    AUTHORIZATION = "AUTHORIZATION", "Authorization"
    PATIENT_DATA = "PATIENT_DATA", "Patient Data"
    CLINICAL = "CLINICAL", "Clinical"
    IMAGING = "IMAGING", "Imaging"
    AI = "AI", "Artificial Intelligence"
    BILLING = "BILLING", "Billing"
    ADMINISTRATION = "ADMINISTRATION", "Administration"
    SECURITY = "SECURITY", "Security"
    SYSTEM = "SYSTEM", "System"


class AuditEvent(models.Model):
    """
    Immutable audit event.

    Audit records must not be modified or deleted through normal
    application operations.

    The event stores enough metadata to reconstruct who performed
    an operation, what was accessed, and when it happened.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    event_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )

    actor = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="audit_events",
    )

    event_type = models.CharField(
        max_length=30,
        choices=AuditEventType.choices,
        db_index=True,
    )

    category = models.CharField(
        max_length=30,
        choices=AuditCategory.choices,
        db_index=True,
    )

    severity = models.CharField(
        max_length=20,
        choices=AuditSeverity.choices,
        default=AuditSeverity.INFO,
        db_index=True,
    )

    action = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    target_model = models.CharField(
        max_length=255,
        blank=True,
    )

    target_object_id = models.CharField(
        max_length=255,
        blank=True,
    )

    target_display = models.CharField(
        max_length=500,
        blank=True,
    )

    request_id = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    endpoint = models.CharField(
        max_length=500,
        blank=True,
    )

    http_method = models.CharField(
        max_length=10,
        blank=True,
    )

    response_status = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    old_values = models.JSONField(
        default=dict,
        blank=True,
    )

    new_values = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        db_table = "audit_events"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "actor",
                    "created_at",
                ],
                name="audit_actor_date_idx",
            ),
            models.Index(
                fields=[
                    "category",
                    "created_at",
                ],
                name="audit_category_date_idx",
            ),
            models.Index(
                fields=[
                    "event_type",
                    "created_at",
                ],
                name="audit_event_date_idx",
            ),
            models.Index(
                fields=[
                    "severity",
                    "created_at",
                ],
                name="audit_severity_date_idx",
            ),
            models.Index(
                fields=[
                    "target_model",
                    "target_object_id",
                ],
                name="audit_target_idx",
            ),
            models.Index(
                fields=[
                    "ip_address",
                    "created_at",
                ],
                name="audit_ip_date_idx",
            ),
        ]

    def save(self, *args, **kwargs):
        """
        Audit records are append-only.

        Existing audit records cannot be updated through Django's
        normal save operation.
        """

        if not self._state.adding:
            raise ValidationError(
                "Audit events are immutable and cannot be modified."
            )

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Prevent normal deletion of audit events.
        """

        raise ValidationError(
            "Audit events are immutable and cannot be deleted."
        )

    def __str__(self):
        return (
            f"{self.event_type} - "
            f"{self.action} - "
            f"{self.created_at}"
        )


class AuthenticationEventType(models.TextChoices):
    LOGIN_SUCCESS = "LOGIN_SUCCESS", "Login Success"
    LOGIN_FAILURE = "LOGIN_FAILURE", "Login Failure"
    LOGOUT = "LOGOUT", "Logout"
    TOKEN_REFRESH = "TOKEN_REFRESH", "Token Refresh"
    PASSWORD_CHANGE = "PASSWORD_CHANGE", "Password Change"
    PASSWORD_RESET_REQUEST = (
        "PASSWORD_RESET_REQUEST",
        "Password Reset Request",
    )
    PASSWORD_RESET_SUCCESS = (
        "PASSWORD_RESET_SUCCESS",
        "Password Reset Success",
    )
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED", "Account Locked"
    ACCOUNT_UNLOCKED = "ACCOUNT_UNLOCKED", "Account Unlocked"


class AuthenticationEvent(models.Model):
    """
    Authentication-specific security events.

    Kept separate from the general audit stream for efficient
    security investigations.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="authentication_events",
    )

    email_attempted = models.EmailField(
        blank=True,
    )

    event_type = models.CharField(
        max_length=40,
        choices=AuthenticationEventType.choices,
        db_index=True,
    )

    success = models.BooleanField(
        default=False,
        db_index=True,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    request_id = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )

    failure_reason = models.CharField(
        max_length=500,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        db_table = "authentication_events"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "user",
                    "created_at",
                ],
                name="auth_event_user_date_idx",
            ),
            models.Index(
                fields=[
                    "email_attempted",
                    "created_at",
                ],
                name="auth_event_email_date_idx",
            ),
            models.Index(
                fields=[
                    "ip_address",
                    "created_at",
                ],
                name="auth_event_ip_date_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.event_type} - "
            f"{self.email_attempted}"
        )


class PatientDataAccessType(models.TextChoices):
    VIEW = "VIEW", "View"
    CREATE = "CREATE", "Create"
    UPDATE = "UPDATE", "Update"
    EXPORT = "EXPORT", "Export"
    DOWNLOAD = "DOWNLOAD", "Download"
    PRINT = "PRINT", "Print"


class PatientDataAccessLog(models.Model):
    """
    Specialized log for access to protected healthcare data.

    This provides an explicit patient-data access trail in addition
    to the general audit event.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    patient = models.ForeignKey(
        "users.PatientProfile",
        on_delete=models.PROTECT,
        related_name="data_access_logs",
    )

    accessed_by = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="patient_data_access_logs",
    )

    access_type = models.CharField(
        max_length=20,
        choices=PatientDataAccessType.choices,
        db_index=True,
    )

    resource_type = models.CharField(
        max_length=255,
    )

    resource_id = models.CharField(
        max_length=255,
    )

    purpose = models.CharField(
        max_length=500,
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    request_id = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        db_table = "patient_data_access_logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "patient",
                    "created_at",
                ],
                name="patient_access_date_idx",
            ),
            models.Index(
                fields=[
                    "accessed_by",
                    "created_at",
                ],
                name="accessor_date_idx",
            ),
            models.Index(
                fields=[
                    "resource_type",
                    "resource_id",
                ],
                name="patient_resource_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.patient.user.full_name} - "
            f"{self.access_type}"
        )


class SecurityEventType(models.TextChoices):
    SUSPICIOUS_LOGIN = (
        "SUSPICIOUS_LOGIN",
        "Suspicious Login",
    )
    RATE_LIMIT = "RATE_LIMIT", "Rate Limit Triggered"
    INVALID_TOKEN = "INVALID_TOKEN", "Invalid Token"
    PERMISSION_DENIED = (
        "PERMISSION_DENIED",
        "Permission Denied",
    )
    UNAUTHORIZED_ACCESS = (
        "UNAUTHORIZED_ACCESS",
        "Unauthorized Access",
    )
    DATA_EXPORT = "DATA_EXPORT", "Data Export"
    FILE_ACCESS = "FILE_ACCESS", "File Access"
    MALICIOUS_REQUEST = (
        "MALICIOUS_REQUEST",
        "Malicious Request",
    )
    SYSTEM_ALERT = "SYSTEM_ALERT", "System Alert"


class SecurityEvent(models.Model):
    """
    Security-focused event stream.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="security_events",
    )

    event_type = models.CharField(
        max_length=40,
        choices=SecurityEventType.choices,
        db_index=True,
    )

    severity = models.CharField(
        max_length=20,
        choices=AuditSeverity.choices,
        default=AuditSeverity.MEDIUM,
        db_index=True,
    )

    description = models.TextField()

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    endpoint = models.CharField(
        max_length=500,
        blank=True,
    )

    request_id = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    resolved = models.BooleanField(
        default=False,
        db_index=True,
    )

    resolved_by = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="security_events_resolved",
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        db_table = "security_events"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "severity",
                    "resolved",
                    "created_at",
                ],
                name="security_open_events_idx",
            ),
            models.Index(
                fields=[
                    "event_type",
                    "created_at",
                ],
                name="security_type_date_idx",
            ),
        ]

    def clean(self):
        if self.resolved and not self.resolved_by:
            raise ValidationError(
                "A resolved security event must have a resolver."
            )

        if not self.resolved and self.resolved_at:
            raise ValidationError(
                "An unresolved security event cannot have "
                "resolved_at."
            )

    def __str__(self):
        return (
            f"{self.event_type} - "
            f"{self.severity}"
        )