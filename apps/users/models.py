import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .managers import UserManager


class TimeStampedModel(models.Model):
    """
    Abstract model providing creation and modification timestamps.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class UserRole(models.TextChoices):
    """
    Roles supported by CuraMind AI.
    """

    PATIENT = "PATIENT", "Patient"
    DOCTOR = "DOCTOR", "Doctor"
    NURSE = "NURSE", "Nurse"
    ADMIN = "ADMIN", "Administrator"
    STAFF = "STAFF", "Staff"
    RADIOLOGIST = "RADIOLOGIST", "Radiologist"
    LAB_TECHNICIAN = "LAB_TECHNICIAN", "Lab Technician"


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """
    Custom application user.

    Email is used as the unique authentication identifier.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    email = models.EmailField(
        unique=True,
        db_index=True,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    role = models.CharField(
        max_length=30,
        choices=UserRole.choices,
        default=UserRole.PATIENT,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    last_login_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["role", "is_active"],
                name="users_role_active_idx",
            ),
            models.Index(
                fields=["last_name", "first_name"],
                name="users_name_idx",
            ),
        ]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """
        Return the user's complete display name.
        """

        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_patient(self):
        return self.role == UserRole.PATIENT

    @property
    def is_doctor(self):
        return self.role == UserRole.DOCTOR

    @property
    def is_nurse(self):
        return self.role == UserRole.NURSE

    @property
    def is_radiologist(self):
        return self.role == UserRole.RADIOLOGIST

    @property
    def is_lab_technician(self):
        return self.role == UserRole.LAB_TECHNICIAN


class Gender(models.TextChoices):
    """
    Gender values used for patient demographic information.
    """

    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHER = "OTHER", "Other"
    PREFER_NOT_TO_SAY = (
        "PREFER_NOT_TO_SAY",
        "Prefer not to say",
    )


class BloodGroup(models.TextChoices):
    """
    Standard ABO/Rh blood groups.
    """

    A_POSITIVE = "A+", "A+"
    A_NEGATIVE = "A-", "A-"
    B_POSITIVE = "B+", "B+"
    B_NEGATIVE = "B-", "B-"
    AB_POSITIVE = "AB+", "AB+"
    AB_NEGATIVE = "AB-", "AB-"
    O_POSITIVE = "O+", "O+"
    O_NEGATIVE = "O-", "O-"


class PatientProfile(TimeStampedModel):
    """
    Healthcare-specific information for a patient.

    Authentication information remains in User while
    healthcare information is isolated in this profile.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="patient_profile",
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    gender = models.CharField(
        max_length=30,
        choices=Gender.choices,
        blank=True,
    )

    blood_group = models.CharField(
        max_length=3,
        choices=BloodGroup.choices,
        blank=True,
    )

    emergency_contact_name = models.CharField(
        max_length=150,
        blank=True,
    )

    emergency_contact_phone = models.CharField(
        max_length=20,
        blank=True,
    )

    emergency_contact_relationship = models.CharField(
        max_length=100,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    medical_record_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
    )

    class Meta:
        db_table = "patient_profiles"

    def __str__(self):
        return self.user.full_name or self.user.email


class DoctorProfile(TimeStampedModel):
    """
    Professional information for doctors and clinical specialists.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="doctor_profile",
    )

    medical_license_number = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    specialization = models.CharField(
        max_length=150,
    )

    qualification = models.CharField(
        max_length=255,
        blank=True,
    )

    years_of_experience = models.PositiveSmallIntegerField(
        default=0,
    )

    hospital_name = models.CharField(
        max_length=255,
        blank=True,
    )

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    is_verified = models.BooleanField(
        default=False,
        db_index=True,
    )

    class Meta:
        db_table = "doctor_profiles"
        indexes = [
            models.Index(
                fields=["specialization", "is_verified"],
                name="doctor_specialty_verified_idx",
            ),
        ]

    def __str__(self):
        return f"Dr. {self.user.full_name}"


class StaffProfile(TimeStampedModel):
    """
    Professional information for non-doctor healthcare staff.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staff_profile",
    )

    employee_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
    )

    department = models.CharField(
        max_length=150,
        blank=True,
    )

    designation = models.CharField(
        max_length=150,
        blank=True,
    )

    class Meta:
        db_table = "staff_profiles"

    def __str__(self):
        return self.employee_id