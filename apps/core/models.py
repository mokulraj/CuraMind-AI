import uuid

from django.core.validators import MinLengthValidator
from django.db import models


class UUIDModel(models.Model):
    """
    Abstract base model providing a UUID primary key.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """
    Abstract base model providing creation and modification timestamps.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Abstract model providing soft-delete support.

    Records are retained in the database instead of being physically
    deleted.
    """

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class BaseModel(
    UUIDModel,
    TimeStampedModel,
    SoftDeleteModel,
):
    """
    Common base model used by CuraMind AI domain entities.
    """

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        abstract = True


class OrganizationType(models.TextChoices):
    """
    Supported healthcare organization types.
    """

    HOSPITAL = "HOSPITAL", "Hospital"
    CLINIC = "CLINIC", "Clinic"
    DIAGNOSTIC_CENTER = (
        "DIAGNOSTIC_CENTER",
        "Diagnostic Center",
    )
    IMAGING_CENTER = (
        "IMAGING_CENTER",
        "Imaging Center",
    )
    LABORATORY = "LABORATORY", "Laboratory"
    OTHER = "OTHER", "Other"


class Organization(BaseModel):
    """
    Healthcare organization or facility using CuraMind AI.
    """

    name = models.CharField(
        max_length=255,
    )

    organization_type = models.CharField(
        max_length=30,
        choices=OrganizationType.choices,
        default=OrganizationType.CLINIC,
        db_index=True,
    )

    registration_number = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "organizations"
        ordering = ["name"]
        indexes = [
            models.Index(
                fields=[
                    "organization_type",
                    "is_active",
                ],
                name="org_type_active_idx",
            ),
        ]

    def __str__(self):
        return self.name


class Department(BaseModel):
    """
    Department belonging to a healthcare organization.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="departments",
    )

    name = models.CharField(
        max_length=150,
    )

    code = models.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(2),
        ],
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "departments"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "name",
                ],
                name="unique_department_name_per_org",
            ),
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "code",
                ],
                name="unique_department_code_per_org",
            ),
        ]
        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "is_active",
                ],
                name="dept_org_active_idx",
            ),
        ]

    def __str__(self):
        return f"{self.organization.name} - {self.name}"


class AddressType(models.TextChoices):
    """
    Address classifications.
    """

    HOME = "HOME", "Home"
    WORK = "WORK", "Work"
    ORGANIZATION = "ORGANIZATION", "Organization"
    OTHER = "OTHER", "Other"


class Address(BaseModel):
    """
    Generic postal address.

    This model is intentionally reusable across healthcare entities.
    """

    address_type = models.CharField(
        max_length=20,
        choices=AddressType.choices,
        default=AddressType.HOME,
    )

    address_line_1 = models.CharField(
        max_length=255,
    )

    address_line_2 = models.CharField(
        max_length=255,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
    )

    state = models.CharField(
        max_length=100,
    )

    postal_code = models.CharField(
        max_length=20,
    )

    country = models.CharField(
        max_length=100,
        default="India",
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "addresses"
        indexes = [
            models.Index(
                fields=[
                    "city",
                    "state",
                ],
                name="address_city_state_idx",
            ),
            models.Index(
                fields=[
                    "postal_code",
                ],
                name="address_postal_code_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.address_line_1}, "
            f"{self.city}, "
            f"{self.state}, "
            f"{self.postal_code}"
        )


class EmergencyContact(BaseModel):
    """
    Emergency contact information.

    Kept independent so the same structure can be reused by
    patient and other healthcare entities.
    """

    full_name = models.CharField(
        max_length=150,
    )

    relationship = models.CharField(
        max_length=100,
    )

    phone_number = models.CharField(
        max_length=20,
    )

    alternate_phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="emergency_contacts",
    )

    class Meta:
        db_table = "emergency_contacts"
        indexes = [
            models.Index(
                fields=[
                    "phone_number",
                ],
                name="emergency_phone_idx",
            ),
        ]

    def __str__(self):
        return self.full_name