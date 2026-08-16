from datetime import date

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.appointments.forms import AppointmentForm
from apps.appointments.models import (
    Appointment,
    AppointmentStatus,
)
from apps.appointments.services.appointment_service import (
    AppointmentService,
)

from apps.dashboard.role_views import role_dashboard

from apps.emr.models import (
    Allergy,
    ClinicalEncounter,
    ClinicalNote,
    Diagnosis,
    MedicalRecord,
    Medication,
    VitalSign,
)
from apps.emr.repositories.medical_record_repository import (
    MedicalRecordRepository,
)
from apps.emr.services.medical_record_service import (
    MedicalRecordService,
)

from apps.notifications.models import Notification

from apps.users.forms import ProfileUpdateForm
from apps.users.models import (
    BloodGroup,
    Gender,
    PatientProfile,
    User,
    UserRole,
)


@login_required
def home(request):
    return role_dashboard(request)


# ==========================================================
# LOGIN
# ==========================================================

def login_page(request):
    """
    Authenticate a user using email and password.

    GET:
        Display the login page.

    POST:
        Authenticate the user and redirect to the dashboard.
    """

    if request.user.is_authenticated:
        return redirect("web:home")

    if request.method == "POST":

        email = request.POST.get(
            "email",
            "",
        ).strip()

        password = request.POST.get(
            "password",
            "",
        )

        user = authenticate(
            request,
            username=email,
            password=password,
        )

        if user is not None:

            login(
                request,
                user,
            )

            messages.success(
                request,
                "You have been logged in successfully.",
            )

            return redirect("web:home")

        messages.error(
            request,
            "Invalid email or password.",
        )

    return render(
        request,
        "auth/login.html",
    )


def logout_view(request):

    logout(request)

    return redirect("web:login")


@login_required
def password_change_page(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST,
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user,
            )

            messages.success(
                request,
                "Your password has been changed successfully.",
            )

            return redirect(
                "web:password-change",
            )

    else:

        form = PasswordChangeForm(
            request.user,
        )

    return render(
        request,
        "auth/password_change.html",
        {
            "form": form,
        },
    )


@login_required
def patients(request):

    search_query = request.GET.get(
        "search",
        "",
    ).strip()

    patients_queryset = (
        PatientProfile.objects
        .select_related("user")
        .filter(
            user__role=UserRole.PATIENT,
        )
        .order_by(
            "user__first_name",
            "user__last_name",
        )
    )

    if search_query:

        patients_queryset = patients_queryset.filter(
            Q(user__first_name__icontains=search_query)
            | Q(user__last_name__icontains=search_query)
            | Q(user__email__icontains=search_query)
            | Q(
                medical_record_number__icontains=search_query
            )
        )

    total_patients = PatientProfile.objects.filter(
        user__role=UserRole.PATIENT,
    ).count()

    active_patients = PatientProfile.objects.filter(
        user__role=UserRole.PATIENT,
        user__is_active=True,
    ).count()

    current_month = timezone.now().date().replace(
        day=1,
    )

    new_this_month = PatientProfile.objects.filter(
        user__role=UserRole.PATIENT,
        created_at__date__gte=current_month,
    ).count()

    patient_rows = []

    for patient in patients_queryset:

        user = patient.user

        age = None

        if patient.date_of_birth:

            today = date.today()

            age = (
                today.year
                - patient.date_of_birth.year
                - (
                    (
                        today.month,
                        today.day,
                    )
                    <
                    (
                        patient.date_of_birth.month,
                        patient.date_of_birth.day,
                    )
                )
            )

        last_appointment = (
            Appointment.objects
            .filter(
                patient=patient,
                status=AppointmentStatus.COMPLETED,
            )
            .select_related("department")
            .order_by(
                "-scheduled_start",
            )
            .first()
        )

        last_visit = None
        department_name = "—"

        if last_appointment:

            last_visit = (
                last_appointment.scheduled_start
            )

            if last_appointment.department:

                department_name = (
                    last_appointment.department.name
                )

        status = (
            "Active"
            if user.is_active
            else "Inactive"
        )

        patient_rows.append(
            {
                "id": patient.id,
                "name": user.full_name,
                "email": user.email,
                "patient_id": patient.medical_record_number,
                "age": age,
                "department": department_name,
                "last_visit": last_visit,
                "status": status,
                "status_class": (
                    "active"
                    if user.is_active
                    else "inactive"
                ),
            }
        )

    return render(
        request,
        "patients.html",
        {
            "patients": patient_rows,
            "total_patients": total_patients,
            "active_patients": active_patients,
            "new_this_month": new_this_month,
            "search_query": search_query,
        },
    )


@login_required
def add_patient(request):

    if request.method == "POST":

        first_name = request.POST.get(
            "first_name",
            "",
        ).strip()

        last_name = request.POST.get(
            "last_name",
            "",
        ).strip()

        email = request.POST.get(
            "email",
            "",
        ).strip().lower()

        phone_number = request.POST.get(
            "phone_number",
            "",
        ).strip()

        date_of_birth = request.POST.get(
            "date_of_birth",
            "",
        ).strip()

        gender = request.POST.get(
            "gender",
            "",
        ).strip()

        blood_group = request.POST.get(
            "blood_group",
            "",
        ).strip()

        medical_record_number = request.POST.get(
            "medical_record_number",
            "",
        ).strip().upper()

        password = request.POST.get(
            "password",
            "",
        )

        confirm_password = request.POST.get(
            "confirm_password",
            "",
        )

        errors = []

        if not first_name:
            errors.append(
                "First name is required."
            )

        if not last_name:
            errors.append(
                "Last name is required."
            )

        if not email:
            errors.append(
                "Email address is required."
            )

        if not medical_record_number:
            errors.append(
                "Medical record number is required."
            )

        if not password:
            errors.append(
                "Password is required."
            )

        if password != confirm_password:
            errors.append(
                "Passwords do not match."
            )

        if len(password) < 8:
            errors.append(
                "Password must contain at least 8 characters."
            )

        if User.objects.filter(
            email__iexact=email,
        ).exists():

            errors.append(
                "A user with this email address already exists."
            )

        if PatientProfile.objects.filter(
            medical_record_number__iexact=medical_record_number,
        ).exists():

            errors.append(
                "This medical record number already exists."
            )

        if gender and gender not in dict(
            Gender.choices,
        ):

            errors.append(
                "Invalid gender selected."
            )

        if blood_group and blood_group not in dict(
            BloodGroup.choices,
        ):

            errors.append(
                "Invalid blood group selected."
            )

        if errors:

            return render(
                request,
                "patients/add_patient.html",
                {
                    "errors": errors,
                    "form_data": request.POST,
                    "gender_choices": Gender.choices,
                    "blood_group_choices": BloodGroup.choices,
                },
            )

        try:

            with transaction.atomic():

                user = User.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    role=UserRole.PATIENT,
                    is_active=True,
                )

                PatientProfile.objects.create(
                    user=user,
                    date_of_birth=(
                        date_of_birth
                        if date_of_birth
                        else None
                    ),
                    gender=gender,
                    blood_group=blood_group,
                    medical_record_number=(
                        medical_record_number
                    ),
                )

        except IntegrityError:

            return render(
                request,
                "patients/add_patient.html",
                {
                    "errors": [
                        "Unable to create patient because "
                        "some information already exists."
                    ],
                    "form_data": request.POST,
                    "gender_choices": Gender.choices,
                    "blood_group_choices": BloodGroup.choices,
                },
            )

        messages.success(
            request,
            f"Patient {first_name} {last_name} "
            "was created successfully.",
        )

        return redirect(
            "web:patients",
        )

    return render(
        request,
        "patients/add_patient.html",
        {
            "gender_choices": Gender.choices,
            "blood_group_choices": BloodGroup.choices,
        },
    )
@login_required
def new_appointment(request):
    """
    Create a new appointment for the authenticated patient.
    """

    # --------------------------------------------------
    # ROLE CHECK
    # --------------------------------------------------

    if request.user.role != UserRole.PATIENT:
        messages.error(
            request,
            "Only patients can book appointments "
            "from this page.",
        )

        return redirect("web:appointments")

    # --------------------------------------------------
    # ==========================================================
# CLINICAL ENCOUNTERS
# ==========================================================

@login_required
@transaction.atomic
def update_clinical_encounter(
    request,
    record_id,
    encounter_id,
):
    """
    Update clinical information for an encounter.
    """

    if request.method != "POST":
        return redirect(
            "web:medical-record-detail",
            record_id=record_id,
        )

    medical_record = (
        MedicalRecord.objects
        .filter(
            id=record_id,
            is_deleted=False,
            is_active=True,
        )
        .first()
    )

    if medical_record is None:
        raise Http404("Medical record not found.")

    encounter = (
        ClinicalEncounter.objects
        .filter(
            id=encounter_id,
            medical_record=medical_record,
            is_deleted=False,
            is_active=True,
        )
        .first()
    )

    if encounter is None:
        raise Http404("Clinical encounter not found.")

    try:
        MedicalRecordService.update_encounter(
            encounter=encounter,
            chief_complaint=request.POST.get(
                "chief_complaint",
                "",
            ).strip(),
            history_of_present_illness=request.POST.get(
                "history_of_present_illness",
                "",
            ).strip(),
            clinical_summary=request.POST.get(
                "clinical_summary",
                "",
            ).strip(),
            examination_notes=request.POST.get(
                "examination_notes",
                "",
            ).strip(),
            treatment_plan=request.POST.get(
                "treatment_plan",
                "",
            ).strip(),
        )

    except ValueError as exc:
        messages.error(
            request,
            str(exc),
        )

        return redirect(
            "web:medical-record-detail",
            record_id=record_id,
        )

    messages.success(
        request,
        "Clinical encounter updated successfully.",
    )

    return redirect(
        "web:medical-record-detail",
        record_id=record_id,
    )


@login_required
@transaction.atomic
def complete_clinical_encounter(
    request,
    record_id,
    encounter_id,
):
    """
    Complete an open clinical encounter.
    """

    if request.method != "POST":
        return redirect(
            "web:medical-record-detail",
            record_id=record_id,
        )

    encounter = (
        ClinicalEncounter.objects
        .filter(
            id=encounter_id,
            medical_record_id=record_id,
            is_deleted=False,
            is_active=True,
        )
        .first()
    )

    if encounter is None:
        raise Http404("Clinical encounter not found.")

    try:
        MedicalRecordService.complete_encounter(
            encounter=encounter,
        )

    except ValueError as exc:
        messages.error(
            request,
            str(exc),
        )

        return redirect(
            "web:medical-record-detail",
            record_id=record_id,
        )

    messages.success(
        request,
        "Clinical encounter completed successfully.",
    )

    return redirect(
        "web:medical-record-detail",
        record_id=record_id,
    )


@login_required
@transaction.atomic
def cancel_clinical_encounter(
    request,
    record_id,
    encounter_id,
):
    """
    Cancel an open clinical encounter.
    """

    if request.method != "POST":
        return redirect(
            "web:medical-record-detail",
            record_id=record_id,
        )

    encounter = (
        ClinicalEncounter.objects
        .filter(
            id=encounter_id,
            medical_record_id=record_id,
            is_deleted=False,
            is_active=True,
        )
        .first()
    )

    if encounter is None:
        raise Http404("Clinical encounter not found.")

    try:
        MedicalRecordService.cancel_encounter(
            encounter=encounter,
        )

    except ValueError as exc:
        messages.error(
            request,
            str(exc),
        )

        return redirect(
            "web:medical-record-detail",
            record_id=record_id,
        )

    messages.success(
        request,
        "Clinical encounter cancelled successfully.",
    )

    return redirect(
        "web:medical-record-detail",
        record_id=record_id,
    )
    
    
    # ==========================================================
    
    
# CLINICAL NOTES
# ==========================================================

@login_required
@transaction.atomic
def create_clinical_note(
    request,
    record_id,
    encounter_id,
):
    """
    Create a clinical note for a medical-record encounter.
    """

    if request.method != "POST":
        return redirect(
            "web:medical-record-detail",
            record_id=record_id,
        )

    medical_record = MedicalRecord.objects.filter(
        id=record_id,
        is_deleted=False,
        is_active=True,
    ).first()

    if medical_record is None:
        raise Http404("Medical record not found.")

    encounter = ClinicalEncounter.objects.filter(
        id=encounter_id,
        medical_record=medical_record,
        is_deleted=False,
        is_active=True,
    ).first()

    if encounter is None:
        raise Http404("Clinical encounter not found.")

    if encounter.status == ClinicalEncounter.Status.COMPLETED:
        messages.error(
            request,
            "Completed clinical encounters cannot be modified.",
        )

        return redirect(
            "web:medical-record-detail",
            record_id=record_id,
        )

    note_type = request.POST.get(
        "note_type",
        "PROGRESS",
    ).strip()

    content = request.POST.get(
        "content",
        "",
    ).strip()

    if not content:
        messages.error(
            request,
            "Clinical note content is required.",
        )

        return redirect(
            "web:medical-record-detail",
            record_id=record_id,
        )

    MedicalRecordService.create_clinical_note(
        encounter=encounter,
        author=request.user,
        note_type=note_type,
        content=content,
        is_signed=False,
    )

    messages.success(
        request,
        "Clinical note created successfully.",
    )

    return redirect(
        "web:medical-record-detail",
        record_id=record_id,
    )


@login_required
@transaction.atomic
def sign_clinical_note(
    request,
    record_id,
    note_id,
):
    """
    Sign an existing clinical note.
    """

    if request.method != "POST":
        return redirect(
            "web:medical-record-detail",
            record_id=record_id,
        )

    medical_record = MedicalRecord.objects.filter(
        id=record_id,
        is_deleted=False,
        is_active=True,
    ).first()

    if medical_record is None:
        raise Http404("Medical record not found.")

    note = (
        ClinicalNote.objects
        .select_related(
            "encounter",
            "encounter__medical_record",
        )
        .filter(
            id=note_id,
            encounter__medical_record=medical_record,
            is_deleted=False,
            is_active=True,
        )
        .first()
    )

    if note is None:
        raise Http404("Clinical note not found.")

    try:
        MedicalRecordService.sign_clinical_note(
            note=note,
        )

    except ValueError as exc:
        messages.error(
            request,
            str(exc),
        )

        return redirect(
            "web:medical-record-detail",
            record_id=record_id,
        )

    messages.success(
        request,
        "Clinical note signed successfully.",
    )

    return redirect(
        "web:medical-record-detail",
        record_id=record_id,
    )
    
    
    # PATIENT PROFILE
    # --------------------------------------------------

    patient = getattr(
        request.user,
        "patient_profile",
        None,
    )

    if patient is None:
        messages.error(
            request,
            "Your patient profile is not available.",
        )

        return redirect("web:appointments")

    # --------------------------------------------------
    # FORM
    # --------------------------------------------------

    if request.method == "POST":

        form = AppointmentForm(
            request.POST
        )

        if form.is_valid():

            try:
                appointment = (
                    AppointmentService.create_appointment(
                        patient=patient,
                        doctor=form.cleaned_data[
                            "doctor"
                        ],
                        scheduled_start=(
                            form.cleaned_data[
                                "scheduled_start"
                            ]
                        ),
                        scheduled_end=(
                            form.get_scheduled_end()
                        ),
                        organization=(
                            form.cleaned_data[
                                "organization"
                            ]
                        ),
                        department=(
                            form.cleaned_data[
                                "department"
                            ]
                        ),
                        appointment_type=(
                            form.cleaned_data[
                                "appointment_type"
                            ]
                        ),
                        consultation_mode=(
                            form.cleaned_data[
                                "consultation_mode"
                            ]
                        ),
                        status="SCHEDULED",
                        reason=(
                            form.cleaned_data[
                                "reason"
                            ]
                        ),
                        symptoms=(
                            form.cleaned_data[
                                "symptoms"
                            ]
                        ),
                    )
                )

            except ValueError as exc:
                form.add_error(
                    None,
                    str(exc),
                )

            else:
                messages.success(
                    request,
                    (
                        "Appointment "
                        f"{appointment.appointment_number} "
                        "was created successfully."
                    ),
                )

                return redirect(
                    "web:appointments"
                )

    else:
        form = AppointmentForm()

    return render(
        request,
        "appointment_new.html",
        {
            "form": form,
        },
    )
    
@login_required
def appointments(request):
    
    """
    Display appointments available to the authenticated user.
    """

    user = request.user

    queryset = (
        Appointment.objects
        .select_related(
            "patient__user",
            "doctor__user",
            "organization",
            "department",
        )
        .filter(
            is_deleted=False,
            is_active=True,
        )
        .order_by(
            "scheduled_start",
        )
    )
    
    

    # --------------------------------------------------
    # ROLE-BASED APPOINTMENT FILTERING
    # --------------------------------------------------

    if user.role == UserRole.PATIENT:

        patient = getattr(
            user,
            "patient_profile",
            None,
        )

        if patient:
            queryset = queryset.filter(
                patient=patient,
            )
        else:
            queryset = queryset.none()

    elif user.role == UserRole.DOCTOR:

        doctor = getattr(
            user,
            "doctor_profile",
            None,
        )

        if doctor:
            queryset = queryset.filter(
                doctor=doctor,
            )
        else:
            queryset = queryset.none()

    elif user.role in {
        UserRole.ADMIN,
        UserRole.STAFF,
        UserRole.NURSE,
    }:
        pass

    else:
        queryset = queryset.none()

    # --------------------------------------------------
    # DATE / STATUS INFORMATION
    # --------------------------------------------------

    now = timezone.now()
    today = now.date()

    today_appointments = (
        queryset
        .filter(
            scheduled_start__date=today,
        )
        .exclude(
            status=AppointmentStatus.CANCELLED,
        )
        .count()
    )

    upcoming_appointments = (
        queryset
        .filter(
            scheduled_start__gt=now,
            status__in=[
                AppointmentStatus.SCHEDULED,
                AppointmentStatus.CONFIRMED,
            ],
        )
        .count()
    )

    completed_appointments = (
        queryset
        .filter(
            status=AppointmentStatus.COMPLETED,
        )
        .count()
    )

    # --------------------------------------------------
    # TABLE DATA
    # --------------------------------------------------

    appointment_rows = []

    for appointment in queryset[:50]:

               appointment_rows.append(
            {
                "id": appointment.id,

                "appointment_number": (
                    appointment.appointment_number
                ),

                "time": (
                    appointment.scheduled_start
                ),

                "patient": (
                    appointment.patient.user.full_name
                ),

                "appointment_type": (
                    appointment.get_appointment_type_display()
                ),

                "consultation_mode": (
                    appointment.get_consultation_mode_display()
                ),

                "provider": (
                    appointment.doctor.user.full_name
                ),

                "organization": (
                    appointment.organization.name
                ),

                "department": (
                    appointment.department.name
                ),

                "status": (
                    appointment.get_status_display()
                ),

                "status_class": (
                    appointment.status.lower()
                ),

                # ------------------------------------------
                # PATIENT ACTION
                # ------------------------------------------

                "can_cancel": (
                    user.role == UserRole.PATIENT
                    and appointment.patient_id
                    == patient.id
                    and appointment.status
                    not in {
                        AppointmentStatus.COMPLETED,
                        AppointmentStatus.CANCELLED,
                    }
                ),

                # ------------------------------------------
                # DOCTOR ACTIONS
                # ------------------------------------------

                "can_confirm": (
                    user.role == UserRole.DOCTOR
                    and appointment.doctor_id
                    == getattr(
                        getattr(
                            user,
                            "doctor_profile",
                            None,
                        ),
                        "id",
                        None,
                    )
                    and appointment.status
                    == AppointmentStatus.SCHEDULED
                ),

                "can_start": (
                    user.role == UserRole.DOCTOR
                    and appointment.doctor_id
                    == getattr(
                        getattr(
                            user,
                            "doctor_profile",
                            None,
                        ),
                        "id",
                        None,
                    )
                    and appointment.status
                    == AppointmentStatus.CONFIRMED
                ),

                "can_complete": (
                    user.role == UserRole.DOCTOR
                    and appointment.doctor_id
                    == getattr(
                        getattr(
                            user,
                            "doctor_profile",
                            None,
                        ),
                        "id",
                        None,
                    )
                    and appointment.status
                    == AppointmentStatus.IN_PROGRESS
                ),
            }
        )
    # --------------------------------------------------
    # RESPONSE
    # --------------------------------------------------

    return render(
        request,
        "appointments.html",
        {
            "appointments": appointment_rows,
            "today_appointments": today_appointments,
            "upcoming_appointments": upcoming_appointments,
            "completed_appointments": completed_appointments,
        },
    )
    
@login_required
def cancel_appointment(request, appointment_id):
    """
    Cancel an appointment belonging to the authenticated patient.
    """

    # --------------------------------------------------
    # METHOD CHECK
    # --------------------------------------------------

    if request.method != "POST":
        return redirect("web:appointments")

    # --------------------------------------------------
    # PATIENT ROLE CHECK
    # --------------------------------------------------

    if request.user.role != UserRole.PATIENT:
        messages.error(
            request,
            "Only patients can cancel appointments.",
        )

        return redirect("web:appointments")

    # --------------------------------------------------
    # PATIENT PROFILE
    # --------------------------------------------------

    patient = getattr(
        request.user,
        "patient_profile",
        None,
    )

    if patient is None:
        messages.error(
            request,
            "Your patient profile is not available.",
        )

        return redirect("web:appointments")

    # --------------------------------------------------
    # GET APPOINTMENT
    # --------------------------------------------------

    appointment = (
        Appointment.objects
        .select_related(
            "patient__user",
            "doctor__user",
            "organization",
            "department",
        )
        .filter(
            id=appointment_id,
            patient=patient,
        )
        .first()
    )

    # --------------------------------------------------
    # SECURITY CHECK
    # --------------------------------------------------

    if appointment is None:
        messages.error(
            request,
            "Appointment not found or you are not "
            "authorized to cancel it.",
        )

        return redirect("web:appointments")

    # --------------------------------------------------
    # CANCELLATION REASON
    # --------------------------------------------------

    reason = request.POST.get(
        "cancellation_reason",
        "",
    ).strip()

    # --------------------------------------------------
    # CANCEL THROUGH SERVICE LAYER
    # --------------------------------------------------

    try:
        AppointmentService.cancel_appointment(
            appointment=appointment,
            reason=reason,
        )

    except ValueError as exc:
        messages.error(
            request,
            str(exc),
        )

    else:
        messages.success(
            request,
            (
                f"Appointment "
                f"{appointment.appointment_number} "
                "was cancelled successfully."
            ),
        )

    return redirect(
        "web:appointments",
    )

@login_required
def confirm_appointment(request, appointment_id):
    """
    Allow the assigned doctor to confirm a scheduled appointment.
    """

    if request.method != "POST":
        return redirect("web:appointments")

    if request.user.role != UserRole.DOCTOR:
        messages.error(
            request,
            "Only doctors can confirm appointments.",
        )
        return redirect("web:appointments")

    doctor = getattr(
        request.user,
        "doctor_profile",
        None,
    )

    if doctor is None:
        messages.error(
            request,
            "Doctor profile is not available.",
        )
        return redirect("web:appointments")

    appointment = (
        Appointment.objects
        .select_related(
            "patient__user",
            "doctor__user",
        )
        .filter(
            id=appointment_id,
            doctor=doctor,
            is_deleted=False,
            is_active=True,
        )
        .first()
    )

    if appointment is None:
        messages.error(
            request,
            "Appointment not found.",
        )
        return redirect("web:appointments")

    try:
        AppointmentService.confirm_appointment(
            appointment=appointment,
        )
    except ValueError as exc:
        messages.error(
            request,
            str(exc),
        )
    else:
        messages.success(
            request,
            (
                f"Appointment "
                f"{appointment.appointment_number} "
                "was confirmed successfully."
            ),
        )

    return redirect("web:appointments")


@login_required
def start_appointment(request, appointment_id):
    """
    Allow the assigned doctor to start a confirmed appointment.
    """

    if request.method != "POST":
        return redirect("web:appointments")

    if request.user.role != UserRole.DOCTOR:
        messages.error(
            request,
            "Only doctors can start appointments.",
        )
        return redirect("web:appointments")

    doctor = getattr(
        request.user,
        "doctor_profile",
        None,
    )

    if doctor is None:
        messages.error(
            request,
            "Doctor profile is not available.",
        )
        return redirect("web:appointments")

    appointment = (
        Appointment.objects
        .select_related(
            "patient__user",
            "doctor__user",
        )
        .filter(
            id=appointment_id,
            doctor=doctor,
            is_deleted=False,
            is_active=True,
        )
        .first()
    )

    if appointment is None:
        messages.error(
            request,
            "Appointment not found.",
        )
        return redirect("web:appointments")

    try:
        AppointmentService.start_appointment(
            appointment=appointment,
        )
    except ValueError as exc:
        messages.error(
            request,
            str(exc),
        )
    else:
        messages.success(
            request,
            (
                f"Appointment "
                f"{appointment.appointment_number} "
                "has started."
            ),
        )

    return redirect("web:appointments")


@login_required
def complete_appointment(request, appointment_id):
    """
    Allow the assigned doctor to complete an appointment
    and save clinical notes.
    """

    if request.method != "POST":
        return redirect("web:appointments")

    if request.user.role != UserRole.DOCTOR:
        messages.error(
            request,
            "Only doctors can complete appointments.",
        )
        return redirect("web:appointments")

    doctor = getattr(
        request.user,
        "doctor_profile",
        None,
    )

    if doctor is None:
        messages.error(
            request,
            "Doctor profile is not available.",
        )
        return redirect("web:appointments")

    appointment = (
        Appointment.objects
        .select_related(
            "patient__user",
            "doctor__user",
        )
        .filter(
            id=appointment_id,
            doctor=doctor,
            is_deleted=False,
            is_active=True,
        )
        .first()
    )

    if appointment is None:
        messages.error(
            request,
            "Appointment not found.",
        )
        return redirect("web:appointments")

    doctor_notes = request.POST.get(
        "doctor_notes",
        "",
    ).strip()

    try:
        AppointmentService.complete_appointment(
            appointment=appointment,
            doctor_notes=doctor_notes,
        )
    except ValueError as exc:
        messages.error(
            request,
            str(exc),
        )
    else:
        messages.success(
            request,
            (
                f"Appointment "
                f"{appointment.appointment_number} "
                "was completed successfully."
            ),
        )

    return redirect("web:appointments")

@login_required
def ai_insights(request):
    return render(
        request,
        "ai_insights.html",
    )


@login_required
def medical_records(request):
    """
    Display medical records available to the
    authenticated user.
    """

    user = request.user

    # --------------------------------------------------
    # GET MEDICAL RECORDS
    # --------------------------------------------------

    if user.role == UserRole.PATIENT:

        patient = getattr(
            user,
            "patient_profile",
            None,
        )

        if patient:
            medical_record = (
                MedicalRecordRepository.get_by_patient(
                    patient.id
                )
            )

            records = (
                [medical_record]
                if medical_record
                else []
            )
        else:
            records = []

    elif user.role in {
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.STAFF,
        UserRole.ADMIN,
    }:

        from apps.emr.models import MedicalRecord

        records = list(
            MedicalRecord.objects
            .select_related(
                "patient__user",
                "primary_physician__user",
            )
            .order_by(
                "-updated_at",
            )
        )

    else:
        records = []

    # --------------------------------------------------
    # STATISTICS
    # --------------------------------------------------

    total_records = len(records)

    active_records = sum(
        1
        for record in records
        if record.status == "ACTIVE"
    )

    updated_today = sum(
        1
        for record in records
        if record.updated_at
        and record.updated_at.date()
        == timezone.localdate()
    )

    # --------------------------------------------------
    # PREPARE TEMPLATE DATA
    # --------------------------------------------------

    record_rows = []

    for record in records:

        patient_name = (
            record.patient.user.full_name
            if record.patient
            and record.patient.user
            else "Unknown Patient"
        )

        physician_name = "Not assigned"

        if record.primary_physician:
            physician_name = (
                record.primary_physician.user.full_name
            )

        record_rows.append(
            {
                "id": record.id,
                "record_number": (
                    record.record_number
                ),
                "patient": patient_name,
                "status": (
                    record.get_status_display()
                ),
                "status_class": (
                    record.status.lower()
                ),
                "summary": (
                    record.summary
                    or "No clinical summary available."
                ),
                "primary_physician": physician_name,
                "created_at": record.created_at,
                "updated_at": record.updated_at,
            }
        )

    # --------------------------------------------------
    # RESPONSE
    # --------------------------------------------------

    return render(
        request,
        "medical_records.html",
        {
            "records": record_rows,
            "total_records": total_records,
            "active_records": active_records,
            "updated_today": updated_today,
        },
    )
    
    
@login_required
def medical_record_detail(request, record_id):
    """
    Display the complete medical record for an authorized user.

    The view is responsible for:
    - Finding the requested medical record.
    - Checking whether the authenticated user can access it.
    - Delegating EMR data retrieval to MedicalRecordService.
    - Passing the complete medical-record summary to the template.
    """

    user = request.user

    # --------------------------------------------------
    # GET MEDICAL RECORD
    # --------------------------------------------------

    record = (
        MedicalRecord.objects
        .select_related(
            "patient__user",
            "primary_physician__user",
        )
        .filter(
            id=record_id,
            is_deleted=False,
            is_active=True,
        )
        .first()
    )

    if record is None:
        raise Http404("Medical record not found.")

    # --------------------------------------------------
    # ACCESS CONTROL
    # --------------------------------------------------

    if user.role == UserRole.PATIENT:

        patient = getattr(
            user,
            "patient_profile",
            None,
        )

        if (
            patient is None
            or record.patient_id != patient.id
        ):
            raise PermissionDenied

    elif user.role in {
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.STAFF,
        UserRole.ADMIN,
    }:
        pass

    else:
        raise PermissionDenied

    # --------------------------------------------------
    # GET COMPLETE MEDICAL RECORD SUMMARY
    # --------------------------------------------------

    summary = MedicalRecordService.get_medical_record_summary(
        medical_record=record,
    )

    # --------------------------------------------------
    # TEMPLATE CONTEXT
    # --------------------------------------------------
    #
    # MedicalRecordService returns the key:
    # "medical_record"
    #
    # The existing template uses:
    # "record"
    #
    # Therefore we preserve "record" here so we do not
    # have to rewrite the template unnecessarily.
    # --------------------------------------------------

    context = {
        **summary,
        "record": record,
        "medical_record": record,
    }

    # --------------------------------------------------
    # RESPONSE
    # --------------------------------------------------

    return render(
        request,
        "medical_record_detail.html",
        context,
    )
    
# ==========================================================
# IMAGING
# ==========================================================

@login_required
def imaging(request):
    """
    Display the medical imaging page.
    """

    return render(
        request,
        "imaging.html",
        {
            "page_title": "Medical Imaging",
        },
    )


# ==========================================================
# REPORTS
# ==========================================================

@login_required
def reports(request):
    """
    Display the reports page.
    """

    return render(
        request,
        "reports.html",
        {
            "page_title": "Reports",
        },
    )


# ==========================================================
# SETTINGS
# ==========================================================

@login_required
def settings_page(request):
    """
    Display the application settings page.
    """

    return render(
        request,
        "settings.html",
        {
            "page_title": "Settings",
        },
    )


# ==========================================================
# LOGIN
# ==========================================================

# ==========================================================
# PASSWORD CHANGE
# ==========================================================

@login_required
def password_change_page(request):
    """
    Allow the authenticated user to change their password.
    """

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST,
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user,
            )

            messages.success(
                request,
                "Your password was changed successfully.",
            )

            return redirect(
                "web:settings",
            )

    else:

        form = PasswordChangeForm(
            request.user,
        )

    return render(
        request,
        "password_change.html",
        {
            "form": form,
        },
    )


# ==========================================================
# LOGOUT
# ==========================================================

@login_required
def logout_view(request):
    """
    Log the current user out of the application.
    """

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully.",
    )

    return redirect(
        "web:login",
    )


# ==========================================================
# NOTIFICATIONS
# ==========================================================

@login_required
def notifications_page(request):
    """
    Display notifications for the authenticated user.
    """

    return render(
        request,
        "notifications.html",
        {
            "page_title": "Notifications",
        },
    )